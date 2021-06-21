import threading
import time
import datetime
import telebot
from main.models import Date


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
                    if today > notify_date and int(now.strftime('%H')) == int(date.visiting_time.strftime('%H')) - 3:
                        participants = date.project.participants
                        for participant in participants:
                            participant.participant
                time.sleep(300)
        except Exception as e:
            print(e)
