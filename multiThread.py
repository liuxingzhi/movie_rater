# this file is used to practice multi-thread in python
# if worked, it will be to used as an alternative to the Doban_crawler file


import time
from queue import Queue
# import threading
from threading import Thread

global my_queue
my_queue = Queue()
STORE_FULL = 20


# con = threading.Condition()


class Producer(Thread):

    def __init__(self, name="producer"):
        Thread.__init__(self)
        self.name = name


    def run(self):
        for i in range(50):
            if my_queue.qsize() > STORE_FULL:
                time.sleep(0.05)
            apple = Apple()
            my_queue.put(apple)
            print(self.name, "produced a new apple, apples in store: ", my_queue.qsize())


class Consumer(Thread):
    def __init__(self, name="consumer"):
        Thread.__init__(self)
        self.name = name

    def run(self):
        for i in range(100):
            if my_queue.empty():
                time.sleep(0.05)
            apple = my_queue.get()
            print(self.name, "consumed an apple, apples in store:", my_queue.qsize())


class Apple:
    def __init__(self):
        color = "red"
        price = 10


def main():
    # p1 = Producer("p1")
    # p2 = Producer("p2")
    # c1 = Consumer("c1")
    # p1.start()
    # p2.start()
    # c1.start()
    # p1.join()
    # p2.join()
    # c1.join()
    l1 = [1,2,3,4,5]
    que = Queue()
    que.put(2)
    a = que.get()
    print(type(a))


if __name__ == '__main__':
    main()
