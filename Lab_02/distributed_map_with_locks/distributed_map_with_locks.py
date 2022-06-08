from multiprocessing import Process
from strategies.optimistic import optimistic_member
from strategies.pessimistic import pessimistic_update_member
from strategies.racy import racy_update_member


if __name__ == '__main__':
    functions = [racy_update_member, pessimistic_update_member, optimistic_member]

    processes = []
    for func in functions:
        process = Process(target=func)
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
