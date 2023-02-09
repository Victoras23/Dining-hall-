import time
import random
import threading

import requests
from flask import Flask, request

from settings import DINNING_HALL_PORT, KITCHEN_PORT, Task

flask_app = Flask(__name__)
FAIL = '\033[91m'
ENDC = '\033[0m'
NR_OF_WORKERS = 6

@flask_app.route('/DinningHall', methods=['POST'])
def DinningHall():
    destination = request.get_json()
    task = Task.dict2task(destination)
    print(f'{FAIL}Dinning hall : Received {task} from Kitchen{ENDC}')
    return {'status_code': 200}

class Worker(threading.Thread):
    def run(self):
        while True:
            task = Task(destination='Kitchen')
            requests.post(
                f'http://localhost:{KITCHEN_PORT}/Kitchen', json=task.task2dict())
            
            time.sleep(random.choice([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]))

def run():
    threads: list[threading.Thread] = []

    server_thread = threading.Thread(target=lambda: flask_app.run(
        port=DINNING_HALL_PORT, debug=False, use_reloader=False))
    threads.append(server_thread)

    for _ in range(NR_OF_WORKERS):
        threads.append(Worker())

    for thread in threads:
        thread.start()


run()