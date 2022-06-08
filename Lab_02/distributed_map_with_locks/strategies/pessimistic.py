import hazelcast


def pessimistic_update_member():
    print("Starting connecting to the Hazelcast client for pessimistic update...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for pessimistic update")

    hz_map = client.get_map("distributed_map_with_locks").blocking()
    print("Created a distributed map for pessimistic update")

    key = "1"
    hz_map.put_if_absent(key, 0)

    print("Starting pessimistic update..")
    for i in range(1000):
        hz_map.lock(key)
        try:
            value = hz_map.get(key)
            value += 1
            hz_map.put(key, value)
        finally:
            hz_map.unlock(key)

    print(f'Finished pessimistic job!\nResult: {hz_map.get(key)}')
    client.shutdown()
