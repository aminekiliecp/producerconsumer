import random
import time
import urllib.request

from queue import Empty, Queue
from threading import Thread

cur_product = 0
max_consumer = 5
done = False

# https://source.unsplash.com/random

list_items = []
for i in range(50):
    list_items.append("https://jsonplaceholder.typicode.com/todos/1")


def produce(queue):
    i = 0
    while True:
        if not list_items:
            # No item in the list, we should notify consumer that there's no item and they should stop.
            for _ in range(max_consumer):
                queue.put("END")
            break
        if queue.full():
            # print("Queue is full, waiting for consumers")
            pass
        else:
            current_item = list_items.pop()
            queue.put(current_item)
            print(f'Produced: {i} ', current_item)
            i += 1

    print('Exiting producer thread...')


def consume(name, queue):
    while not done:
        try:
            current_item = queue.get()
            if current_item == "END":
                print(f"consumer {name} is ending")
                break
            contents = urllib.request.urlopen(current_item).read()
            queue.task_done()
            print('{} consumed: {}'.format(name, current_item))
            time.sleep(random.randint(0, 5))
        except Empty:
            pass

    print('Exiting consumer thread', name)


def main():
    q = Queue(max_consumer)

    producer = Thread(target=produce, args=(q,))
    producer.start()

    consumers = []
    for i in range(max_consumer):
        name = 'Consumer-{}'.format(i)
        consumer = Thread(target=consume, args=(name, q))
        consumer.start()
        consumers.append(consumer)

    producer.join()

    for consumer in consumers:
        consumer.join()
    print('Ending execution')


if __name__ == '__main__':
    main()
