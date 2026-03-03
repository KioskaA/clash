import random
import time

class DataGenerator:
    pass

def sleep(ms, text=False):
    if text:
        print(f"Засыпаем на {ms} миллисекунд")
        time.sleep(ms/1000)
        print(f"Проснулись")
    else:
        time.sleep(ms/1000)