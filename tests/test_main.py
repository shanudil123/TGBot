from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Define states
NAME, EMAIL, TICKETS = range(3)

# Start registration process
def start_registration(update: Update, context: CallbackContext):
    update.message.reply_text('Please enter your name:')
    return NAME

# Collect name
def collect_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    update.message.reply_text('Please enter your email:')
    return EMAIL

# Collect email
def collect_email(update: Update, context: CallbackContext):
    context.user_data['email'] = update.message.text
    update.message.reply_text('How many tickets do you need?')
    return TICKETS

# Collect tickets and confirm registration
def collect_tickets(update: Update, context: CallbackContext):
    context.user_data['tickets'] = update.message.text
    update.message.reply_text('Thank you for registering!')

    # Store user info in database
    user_info = {
        'name': context.user_data['name'],
        'email': context.user_data['email'],
        'tickets': context.user_data['tickets']
    }
    # Save user_info to database (to be implemented)

    # Add user to group (to be implemented)

    return ConversationHandler.END

def main():
    # Create the Application and pass the bot's token
    application = Application.builder().token('7155095191:AAECu8Sn9FIG6nl7tsba_vK_8pB-Cru-BUE').build()

    # Define the registration handler
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('register', start_registration)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, collect_name)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, collect_email)],
            TICKETS: [MessageHandler(Filters.text & ~Filters.command, collect_tickets)],
        },
        fallbacks=[]
    )

    # Add the registration handler to the application
    application.add_handler(registration_handler)

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()
