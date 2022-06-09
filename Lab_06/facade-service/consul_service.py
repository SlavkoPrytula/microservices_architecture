import argparse
# import uuid
import consul
import hazelcast


class Consul:
    # consul_common wrapper
    def __init__(self, port):
        self.port = port
        self.consul = consul.Consul(host='localhost', port=8500)

        self.services = self.consul.agent.services()
        self.hazelcast = self.connect_hazelcast()

    def register_service(self, service_name, port, service_id):
        self.consul.agent.service.register(service_name, port=port, service_id=service_id)

    def connect_hazelcast(self):
        hz_client = hazelcast.HazelcastClient(cluster_name="dev",
                                              cluster_members=self.consul.kv.get('hazelcast_ports')[1]['Value'].decode(
                                                  "utf-8").split())
        return hz_client

    def hazelcast_map(self):
        print("Connected to the hz clusters")

        _map = self.hazelcast.get_map(self.consul.kv.get('map')[1]['Value'].decode("utf-8")).blocking()
        return _map

    def hazelcast_queue(self):
        print("Connected to the hz clusters")
        _queue = self.hazelcast.get_queue(self.consul.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()
        return _queue


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int)
    args = parser.parse_args()

    consul = Consul(args.port)
