import argparse
import hazelcast
from flask import Flask, request

# Flask app
app = Flask(__name__)
data = list()

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)
args = parser.parse_args()

client = hazelcast.HazelcastClient()
print("Connected to hz clusters")

messages_queue = client.get_queue("my-bounded-queue").blocking()


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
