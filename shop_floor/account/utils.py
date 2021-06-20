from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import telebot


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.username) + text_type(timestamp)


token_generator = AppTokenGenerator()


def check_telegram_id(user_id):
    bot = telebot.TeleBot('1890824375:AAErbP1HmkhidoXqYlhWlYx1iLivGd98ZXE')
    try:
        bot.send_message(user_id, 'Ничего не отвечайте на это сообщение\nЭто только проверка')
        return True
    except:
        return False


def return_correct_phone(phone):
    phone = str(phone)
    if phone[0] == '9':
        phone = '+7' + phone
    elif phone[0] == '8':
        phone = '+7' + phone[1:]
    elif phone[0] == '7':
        phone = '+' + phone
    return phone
