import argparse
from random import choice
import uuid
import hazelcast
import requests
from flask import Flask, request

# Flask app
app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)
args = parser.parse_args()

client = hazelcast.HazelcastClient()
print("Connected to hz clusters")

messages_queue = client.get_queue("my-bounded-queue").blocking()


logging_services = ["http://localhost:8083/logging",
                    "http://localhost:8084/logging",
                    "http://localhost:8085/logging"]

message_services = ["http://localhost:8081/messages",
                    "http://localhost:8082/messages"]


@app.route("/facade", methods=['POST', 'GET'])
def facade():
    if request.method == 'POST':
        # message service
        _msg = request.json.get("msg", None)
        messages_queue.put(f"{_msg}")

        # logging service
        msg = {"uuid": uuid.uuid4(), "msg": _msg}
        response = requests.post(choice(logging_services), data=msg)
        return response.text

    elif request.method == 'GET':
        # messages from logging service
        logging_response = requests.get(choice(logging_services))

        # responses from messages service
        messages_response = requests.get(choice(message_services))

        return f"Logging Service:\t{logging_response}\nMessages Service:\t{messages_response}"


if __name__ == "__main__":
    app.run(host='localhost', port=args.port)
