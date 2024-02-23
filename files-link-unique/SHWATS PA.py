import telebot # pip install pyTelegramBotAPI
import os
from keep_alive import keep_alive
keep_alive()

TOKEN = "6840829556:AAErvmLhFVDPFUsSzWURIT9g12bdaIxNzrM" # replace with your bot token
CHANNEL_ID = "-1002022252775" # replace with your channel ID
UPDATE_CHANNEL_ID = "-1002102435643" # replace with your update channel ID
AUTHORIZED_USER_ID = 6897230899 # replace with your authorized user ID
bot = telebot.TeleBot(TOKEN)

# A dictionary to store user data
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello, I'm a file sharing bot created by SHWAT. You can Recive Files Shared By SHWAT")

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])
def handle_files(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        # Forward the file to the channel
        forwarded_message = bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
        
        # Get the file ID of the file in the channel
        if message.content_type == 'document':
            channel_file_id = forwarded_message.document.file_id
        elif message.content_type == 'photo':
            # Telegram sends photos in different sizes, we'll use the largest one
            channel_file_id = forwarded_message.photo[-1].file_id
        elif message.content_type == 'audio':
            channel_file_id = forwarded_message.audio.file_id
        elif message.content_type == 'video':
            channel_file_id = forwarded_message.video.file_id
        
        bot.send_message(message.chat.id, f"{channel_file_id}")
    else:
        bot.send_message(message.chat.id, "Don't send me files.")

@bot.message_handler(func=lambda message: True)
def track_users_and_send_file(message):
    # Track user data
    user_data[message.from_user.id] = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    # Ignore commands
    if message.text.startswith('/'):
        return

    try:
        # Check if the user is a member of the update channel
        user_status = bot.get_chat_member(UPDATE_CHANNEL_ID, message.from_user.id)
        if user_status.status not in ["creator", "administrator", "member"]:
            bot.send_message(message.chat.id, "Please join the Update Channel to get your file. https://t.me/+lKjcWcpSK8AzYzQ1")
            return

        bot.send_document(message.chat.id, message.text)
    except Exception as e:
        bot.send_message(message.chat.id, "Sorry, I couldn't find a file with that ID.")

@bot.message_handler(commands=['get_users'])
def get_users(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        if not user_data:  # Check if the dictionary is empty
            bot.send_message(message.chat.id, "Users not available.")
        else:
            for user_id, user_info in user_data.items():
                bot.send_message(message.chat.id, f"User ID: {user_id}, Username: {user_info['username']}, First Name: {user_info['first_name']}, Last Name: {user_info['last_name']}")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command. Only SHWAT can use this")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        broadcast_message = message.text.split(' ', 1)[1]  # Get the message text after the command
        for user_id in user_data.keys():
            try:
                bot.send_message(user_id, broadcast_message)
            except Exception as e:
                print(f"Couldn't send message to {user_id}.")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command. Only SHWAT can use this")

bot.polling()