from telebot import TeleBot


def init_bot(token: str) -> TeleBot:
    return TeleBot(token)
