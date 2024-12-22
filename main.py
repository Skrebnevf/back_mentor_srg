from config import load_config
from bot import init_bot
from database import init_db, add_user, get_user, delete_user, update_user, record_message
from telebot.types import Message


config = load_config()
db = init_db(config['SUPABASE_URL'], config['SUPABASE_API_KEY'])
bot = init_bot(config['BOT_TOKEN'])


@bot.message_handler(commands=['start'])
def start_command(message: Message) -> None:
    tg_user = message.from_user
    our_user = get_user(db, tg_user.id)    
    if our_user:
        bot.reply_to(message, f"Привет, я знаю тебя, ты {our_user['name']}.")
    else:
        add_user(db, tg_user.id, tg_user.username, tg_user.first_name, tg_user.last_name)
        bot.reply_to(message, f"Привет, {tg_user.first_name}!")


@bot.message_handler(commands=['forget_me'])
def forget_me_command(message: Message) -> None:
    tg_user = message.from_user
    our_user = get_user(db, tg_user.id)    
    if our_user:
        delete_user(db, our_user['id'])
        bot.reply_to(message, f"Я забыл тебя...")
    else:
        bot.reply_to(message, f"Я не знаю тебя... Жми /start и я тебя запомню")


@bot.message_handler(commands=['help'])
def forget_me_command(message: Message) -> None:
    bot.reply_to(message, '/start\n/forget_me\n/help\n/update_my_info')


@bot.message_handler(commands=['update_my_info'])
def update_my_info_command(message: Message) -> None:
    tg_user = message.from_user
    our_user = get_user(db, tg_user.id)    
    if our_user:
        resp = update_user(db, tg_user.id, tg_user.username, tg_user.first_name, tg_user.last_name)
        bot.reply_to(message, resp)
    else:
        bot.reply_to(message, f"Я не знаю тебя... Жми /start и я тебя запомню")


@bot.message_handler(content_types=["text"])
def handle_text(message: Message) -> None:
    record_message(db, message.from_user.id, message.text)
    bot.send_message(message.chat.id, 'Я запишу это...')


if __name__ == "__main__":
    print('Бот запускается...')
    bot.infinity_polling()
