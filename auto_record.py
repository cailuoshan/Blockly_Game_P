import requests
import schedule
from datetime import datetime


def record():
    response = requests.get('http://zh.codestraveler.tech/study/auto_record')
    today = datetime.now()
    print(f'{response} in {today.strftime("%Y/%m/%d")}')


schedule.every().day.at('09:00').do(record)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
