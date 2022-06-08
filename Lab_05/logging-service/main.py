# from Lab_04.hazelcast.main import messages
import hazelcast

hz_client = hazelcast.HazelcastClient()
messages = hz_client.get_map("distributed_messages_map").blocking()


def get_messages():
    return messages


def post_message(message_data):
    messages.put(message_data["message_uuid"], message_data["message"])

    return {
        "statusCode": 200
    }
