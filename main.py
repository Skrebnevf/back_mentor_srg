from config import load_config
from bot import init_bot
from database import init_db, add_user, get_user

config = load_config()
db = init_db(config['SUPABASE_URL'], config['SUPABASE_API_KEY'])
bot = init_bot(config['BOT_TOKEN'])

@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user
    existing_user = get_user(db, user.id)

    if existing_user:
        bot.reply_to(message, "Hi i know, you faggot")
    else:
        add_user(db, user.id, user.username, user.first_name, user.last_name)
        bot.reply_to(message, "Hi Faggot")


if __name__ == "__main__":
    bot.infinity_polling()
