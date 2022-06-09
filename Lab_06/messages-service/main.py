import argparse
import uuid

from consul_service import Consul
from flask import Flask, request

# Flask app
app = Flask(__name__)
data = list()

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)
args = parser.parse_args()

consul = Consul(args.port)
consul.register_service(
    service_name='messages-service',
    port=args.port,
    service_id=f"messages-{str(uuid.uuid4())}"
)

messages_queue = consul.hazelcast_queue()


@app.route("/messages", methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        print(messages_queue.take())
        while not messages_queue.is_empty():
            data.append(messages_queue.take())
            print("Messages Service: ", data[-1])
        return ",".join(data)
    return f"{request.method} error!"


if __name__ == "__main__":
    app.run(host='localhost', port=args.port)
