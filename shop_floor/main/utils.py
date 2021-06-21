import threading
import time
import datetime
import telebot
from main.models import Date
from django.core.mail import EmailMessage


class SendNotificationThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('Поток запустился')
        try:
            while 1:
                dates = Date.objects.filter(notify_send=False)
                today = datetime.date.today()
                now = datetime.datetime.now()
                for date in dates:
                    notify_date = date.visiting_date - datetime.timedelta(7)
                    if today > notify_date or (today == notify_date and
                                               int(now.strftime('%H')) == int(date.visiting_time.strftime('%H')) - 3):
                        message_title = 'Напоминалка для смен'
                        message_text = f'У тебя смена {date.visiting_date} в {date.visiting_time.strftime("%H:%M")}\n' \
                                       f'Проект: {date.project}\n' \
                                       f'Адресс: {date.address}\n' \
                                       f'Сеттинг: {date.setting}\n' \
                                       f'Сцены: {date.scene}'
                        participants = date.project.participants.all()
                        users = set()
                        for participant in participants:
                            users.add(participant.participant)
                        for participant in users:
                            message_text = f'Привет, {participant}\n' + message_text
                            if participant.telegram_notify:
                                bot = telebot.TeleBot('1890824375:AAErbP1HmkhidoXqYlhWlYx1iLivGd98ZXE')
                                try:
                                    bot.send_message(participant.telegram_id, message_text)
                                except:
                                    bot.send_message(
                                        date.project.admin.telegram_id,
                                        f'Не смог отпрваить сообщение пользователю {participant}'
                                    )
                            if participant.mail_notify:
                                email = EmailMessage(message_title, message_text, 'noreply@semycolon.com',
                                                     [participant.email], )
                                email.send(fail_silently=False)
                        date.notify_send = True
                        date.save()

                time.sleep(300)
        except Exception as e:
            print(e)
