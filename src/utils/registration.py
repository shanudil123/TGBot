import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# Load configuration
with open('D:/bot/TGBot/src/config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['token']

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Set to DEBUG for detailed logging
)

# Define states
NAME, EMAIL, TICKETS = range(3)

# Start registration process
async def start_registration(update: Update, context: CallbackContext):
    logging.debug("Received /register command")
    await update.message.reply_text('Please enter your name:')
    return NAME

# Collect name
async def collect_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    logging.debug(f"Collected name: {context.user_data['name']}")
    await update.message.reply_text('Please enter your email:')
    return EMAIL

# Collect email
async def collect_email(update: Update, context: CallbackContext):
    context.user_data['email'] = update.message.text
    logging.debug(f"Collected email: {context.user_data['email']}")
    await update.message.reply_text('How many tickets do you need?')
    return TICKETS

# Collect tickets and confirm registration
async def collect_tickets(update: Update, context: CallbackContext):
    context.user_data['tickets'] = update.message.text
    logging.debug(f"Collected tickets: {context.user_data['tickets']}")
    await update.message.reply_text('Thank you for registering!' + 'https://t.me/+wUusYLJ3Bck4NDFl')

    # Store user info in database (to be implemented)
    user_info = {
        'name': context.user_data['name'],
        'email': context.user_data['email'],
        'tickets': context.user_data['tickets']
    }
    logging.debug(f"User info: {user_info}")
    # Save user_info to database (to be implemented)

    # Add user to group (to be implemented)

    return ConversationHandler.END

# Fallback handler
async def fallback(update: Update, context: CallbackContext):
    logging.debug("Fallback triggered")
    await update.message.reply_text("I didn't understand that. Please use /register to start the registration process.")

def main():
    logging.debug("Starting bot")

    # Create the Application and pass the bot's token
    application = Application.builder().token(TOKEN).build()

    # Define the registration handler
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('register', start_registration)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_email)],
            TICKETS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_tickets)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, fallback)],
        allow_reentry=True
    )

    # Add the registration handler to the application
    application.add_handler(registration_handler)

    # Add a start command handler
    async def start(update: Update, context: CallbackContext):
        await update.message.reply_text('Welcome! Use /register to get your free ticket.')
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Add a help command handler
    async def help_command(update: Update, context: CallbackContext):
        await update.message.reply_text('Use /start to get event details, /register to get tickets.')

    help_handler = CommandHandler('help', help_command)
    application.add_handler(help_handler)

    # Start polling for updates
    logging.debug("Starting polling")
    application.run_polling()

if __name__ == '__main__':
    main()
