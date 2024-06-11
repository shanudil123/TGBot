from telegram import Bot
import json

def get_group_invite_link():
    with open('D:/bot/TGBot/src/config.json') as config_file:
        config = json.load(config_file)
    bot = Bot(token=config['token'])
    group_id = config['group_id']
    
    # Generate a new invite link
    invite_link = bot.export_chat_invite_link(chat_id=group_id)
    return invite_link


