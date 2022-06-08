# from ..hazelcast.main import messages
import hazelcast
hz_client = hazelcast.HazelcastClient()
messages = hz_client.get_queue("distributed_messages_queue").blocking()


def consumer():
    items = []
    while not messages.is_empty():
        item = messages.take()
        items.append(item["message"])
    return items


def producer(message):
    messages.put(message)

    return {
        "statusCode": 200
    }
