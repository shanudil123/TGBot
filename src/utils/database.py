import json

def save_user_info(user_info):
    with open('D:/bot/TGBot/user_data.json', 'r+') as db_file:
        data = json.load(db_file)
        data['users'].append(user_info)
        db_file.seek(0)
        json.dump(data, db_file, indent=4)


