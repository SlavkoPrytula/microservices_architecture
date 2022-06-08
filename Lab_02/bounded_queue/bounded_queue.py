import sys
# sys.path.insert(0, r"c:\users\user\appdata\local\schrodinger\pymol2\lib\site-packages")

import hazelcast
from multiprocessing import Process


def producer(proc_id):
    print("Starting connecting to the Hazelcast client for producer...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for producer")

    queue = client.get_queue("distributed_queue").blocking()
    print("Created a distributed queue for [producer]")

    for i in range(100):
        item = f'{i} value'
        queue.put(item)
        print(f'Produced: {item} at process: {proc_id}')

    queue.put(-1)
    print("Producer finished!")


def consumer(proc_id):
    print("Starting connecting to the Hazelcast client for consumer...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for consumer")

    queue = client.get_queue("distributed_queue").blocking()
    print("Created a distributed queue for [consumer]")

    while True:
        item = queue.take()
        print(f'Consumed: {item} at process: {proc_id}')
        print("Consumed: ", item, ". Process: ", proc_id)
        if item == -1:
            queue.put(-1)
            break

    print("Consumer finished!")


if __name__ == '__main__':
    functions = [producer, producer, consumer, consumer]
    processes = []

    for i, func in enumerate(functions):
        process = Process(target=func, args=(i,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
