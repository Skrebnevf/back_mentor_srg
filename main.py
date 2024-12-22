from posix import write
from config import load_config
from bot import init_bot
from database import init_db, get_taric, write_taric, add_user, get_user, delete_user, update_user, record_message
from external import get_tariff_number
import re


config = load_config()
db = init_db(config['SUPABASE_URL'], config['SUPABASE_API_KEY'])
bot = init_bot(config['BOT_TOKEN'])


@bot.message_handler(commands=['start'])
def start_command(message) -> None:
    tg_user = message.from_user
    our_user = get_user(db, tg_user.id)
    if our_user:
        bot.reply_to(message, f"Привет, я знаю тебя, ты {our_user['name']}.")
    else:
        add_user(db, tg_user.id, tg_user.username, tg_user.first_name, tg_user.last_name)
        bot.reply_to(message, f"Привет, {tg_user.first_name}!")


@bot.message_handler(commands=['forget_me'])
def forget_me_command(message) -> None:
    tg_user = message.from_user
    our_user = get_user(db, tg_user.id)
    if our_user:
        delete_user(db, our_user['id'])
        bot.reply_to(message, f"Я забыл тебя...")
    else:
        bot.reply_to(message, f"Я не знаю тебя... Жми /start и я тебя запомню")

@bot.message_handler(commands=['code'])
def code_command(message):
    bot.reply_to(message, "Введите код формата XXXXXX или больше 6ти знаков")
    bot.register_next_step_handler(message, process_code)

def process_code(message):
   code = message.text.replace(" ", "")
   result = get_taric(db, code)

   if result:
       description = result.get("description")
       bot.reply_to(message, f"Description - {description}")
   else:
       external_result = get_tariff_number(code)
       if external_result:
           external_description = external_result.get("suggestions")
           external_description = external_description[0].get("value")
           external_description = re.sub(r'<.*?>', '', external_description)
           bot.reply_to(message, f"Description - {external_description}")
           write_taric(db, code, external_description)


@bot.message_handler(commands=['help'])
def help_command(message) -> None:
    bot.reply_to(message, '/start\n/forget_me\n/help\n/update_my_info')


@bot.message_handler(commands=['update_my_info'])
def update_my_info_command(message) -> None:
    tg_user = message.from_user
    our_user = get_user(db, tg_user.id)
    if our_user:
        resp = update_user(db, tg_user.id, tg_user.username, tg_user.first_name, tg_user.last_name)
        bot.reply_to(message, resp)
    else:
        bot.reply_to(message, f"Я не знаю тебя... Жми /start и я тебя запомню")


@bot.message_handler(content_types=["text"])
def handle_text(message) -> None:
    record_message(db, message.from_user.id, message.text)
    bot.send_message(message.chat.id, 'Я запишу это...')


if __name__ == "__main__":
    print('Бот запускается...')
    bot.infinity_polling()
