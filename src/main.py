import json
import logging
import uuid  # For generating unique IDs
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler

# Define states for conversation handler
NAME, EMAIL, TICKETS, CONFIRM = range(4)

# Load configuration
with open('E:/self study/organized - Copy/src/config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['token']

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Start bot
application = Application.builder().token(TOKEN).build()

# Helper functions

def get_event_details() -> str:
    return "Welcome! Use /register to get your free ticket."

def get_group_invite_link():
    from telegram import Bot
    with open('E:/self study/organized - Copy/src/config.json') as config_file:
        config = json.load(config_file)
    bot = Bot(token=config['token'])
    group_id = config['group_id']
    
    # Generate a new invite link
    invite_link = bot.export_chat_invite_link(chat_id=group_id)
    return invite_link

async def register_user(update: Update, user_info: dict) -> None:
    unique_id = f"{user_info['name']}-{user_info['email']}"
    await update.message.reply_text(f"Registration successful! Your ticket ID is {unique_id}.")

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(get_event_details())

# Register command handler
async def register(update: Update, context: CallbackContext):
    await update.message.reply_text("Please enter your name:")
    return NAME

# Conversation handlers for registration
async def collect_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Please enter your email:")
    return EMAIL

async def collect_email(update: Update, context: CallbackContext):
    context.user_data['email'] = update.message.text
    await update.message.reply_text("How many tickets do you need?")
    return TICKETS

async def collect_tickets(update: Update, context: CallbackContext):
    context.user_data['tickets'] = int(update.message.text)
    
    # Confirm the request with inline buttons
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='yes'),
            InlineKeyboardButton("No", callback_data='no')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Please confirm your request:\n\n"
        f"Name: {context.user_data['name']}\n"
        f"Email: {context.user_data['email']}\n"
        f"Tickets: {context.user_data['tickets']}\n\n"
        f"Send 'Yes' to confirm or 'No' to cancel.",
        reply_markup=reply_markup
    )
    return CONFIRM

async def confirm(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    confirmation = query.data.lower()
    if confirmation == 'yes':
        unique_id = str(uuid.uuid4())[:8]
        context.user_data['unique_id'] = unique_id

        # Generate the invite link
        invite_link = get_group_invite_link()
        await query.edit_message_text(
            f"Thank you for registering! Your unique ID is {unique_id}.\n\n"
            f"Join the group using this link: https://t.me/+wUusYLJ3Bck4NDFl\n")

        user_info = {
            'name': context.user_data['name'],
            'email': context.user_data['email'],
            'tickets': context.user_data['tickets']
        }

        # Save user_info to a JSON file
        with open('user_data.json', 'a') as file:
            json.dump(user_info, file)
            file.write('\n')  # Add a newline for each entry         
                    
    else:
        await query.edit_message_text("Registration cancelled.")
    
    return ConversationHandler.END

# Help command handler
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Use /start to get event details, /register to request tickets.")

# Main function to set up the bot
def main():
    # Initialize conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_email)],
            TICKETS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_tickets)],
            CONFIRM: [CallbackQueryHandler(confirm)]
        },
        fallbacks=[CommandHandler('cancel', lambda update, context: update.message.reply_text("Registration cancelled."))]
    )

    # Add handlers to application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()
