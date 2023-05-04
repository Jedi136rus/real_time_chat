import time
import random

import requests

if __name__ == '__main__':
    actions = ['view', 'click', 'close']

    while True:
        action = 'view'
        answer = requests.post(f'http://127.0.0.1:5000/event')
        print(answer.status_code)
        time.sleep(4)
