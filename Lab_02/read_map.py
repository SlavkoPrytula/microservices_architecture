import hazelcast


def main():
    # Start Hazelcast client
    print("Starting connecting to the Hazelcast client...")
    hz = hazelcast.HazelcastClient()
    hz1 = hazelcast.HazelcastClient()
    print("Connected to the Hazelcast client")

    # Get the Distributed Map from Cluster.
    hz_map = hz.get_map("distributed_map").blocking()
    print("Created a distributed map")

    for key, value in hz_map.entry_set():
        print(key, value)

    print(f'\nTotal map size: {len(hz_map.entry_set())}')

    key_id = 1
    entry = hz1.get_map("distributed_map").get_entry_view(key_id).result()
    print(f'\nINFO for key {key_id}')
    print('-' * 15)
    print("size in memory  :", entry.cost)
    print("creationTime    :", entry.creation_time)
    print("expirationTime  :", entry.expiration_time)
    print("number of hits  :", entry.hits)
    print("lastAccessedTime:", entry.last_access_time)
    print("lastUpdateTime  :", entry.last_update_time)
    print("version         :", entry.version)
    print("key             :", entry.key)
    print("value           :", entry.value)

    hz.shutdown()


if __name__ == "__main__":
    main()
