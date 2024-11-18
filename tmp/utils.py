import time
import random

def time_sleep(a: int, b: int):
    random_num = random.uniform(a, b)
    time.sleep(random_num)