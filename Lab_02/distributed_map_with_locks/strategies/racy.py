import hazelcast


def racy_update_member():
    print("Starting connecting to the Hazelcast client for racy update...")
    client = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client for racy update")

    hz_map = client.get_map("distributed_map_with_locks").blocking()
    print("Created a distributed map for racy update")

    key = "1"
    hz_map.put_if_absent(key, 0)

    print("Starting racy update...")
    for i in range(1000):
        value = hz_map.get(key)
        value += 1
        hz_map.put(key, value)

    print(f'Finished racy job!\nResult: {hz_map.get(key)}')
    client.shutdown()
