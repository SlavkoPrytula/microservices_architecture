import argparse
from consul_service import Consul
from random import choice
import uuid
import requests
from flask import Flask, request

# Flask app
app = Flask(__name__)

# finding logging and messages clients
logging_clients = []
messages_clients = []

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)
args = parser.parse_args()


consul = Consul(args.port)
consul.register_service(
    service_name='facade-service',
    port=args.port,
    service_id=f"facade-{str(uuid.uuid4())}"
)

messages_queue = consul.hazelcast_queue()

for key, value in consul.services.items():
    service_name = key.split("-")[0]
    print(service_name)

    if service_name == "logging":
        logging_clients.append(f"http://localhost:{value['Port']}/logging")
    elif service_name == "messages":
        messages_clients.append(f"http://localhost:{value['Port']}/messages")


@app.route("/facade", methods=['POST', 'GET'])
def facade():
    if request.method == 'POST':
        # message service
        _msg = request.json.get("msg", None)
        messages_queue.put(f"{_msg}")

        # logging service
        msg = {"uuid": uuid.uuid4(), "msg": _msg}
        response = requests.post(choice(logging_clients), data=msg)
        return response.text

    elif request.method == 'GET':
        logging_response = ''
        messages_response = ''

        # messages from logging service
        logging_response = requests.get(choice(logging_clients))

        # responses from messages service
        print(choice(messages_clients))
        messages_response = requests.get(choice(messages_clients))

        return f"Logging Service:\t{logging_response}\nMessages Service:\t{messages_response}"


if __name__ == "__main__":
    app.run(host='localhost', port=args.port)
# if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--port', type=int)
    # args = parser.parse_args()
    #
    # consul = Consul(args.port)
    # consul.register_service(
    #     service_name='facade-service',
    #     port=args.port,
    #     service_id=f"facade-{str(uuid.uuid4())}"
    # )
    #
    # messages_queue = consul.hazelcast_queue()
    #
    # app.run(host='localhost', port=args.port)
    #
    # for key, value in consul.services.items():
    #     service_name = key.split("-")[0]
    #
    #     if service_name == "logging":
    #         logging_clients.append(f"http://localhost:{value['Port']}/logging")
    #     elif service_name == "messages":
    #         messages_clients.append(f"http://localhost:{value['Port']}/messages")
