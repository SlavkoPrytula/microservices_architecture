import hazelcast
from copy import deepcopy


def optimistic_member():
    print("Starting connecting to the Hazelcast client for optimistic update...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for optimistic update")

    hz_map = client.get_map("distributed_map_with_locks").blocking()
    print("Created a distributed map for optimistic update")

    key = "1"
    hz_map.put_if_absent(key, 0)

    print("Starting optimistic update...")
    for i in range(1000):
        while True:
            old_value = hz_map.get(key)
            new_value = deepcopy(old_value)
            new_value += 1
            if hz_map.replace_if_same(key, old_value, new_value):
                break

    print(f'Finished optimistic job!\nResult: {hz_map.get(key)}')
    client.shutdown()
