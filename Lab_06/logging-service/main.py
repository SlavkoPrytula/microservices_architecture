import argparse
import uuid

from consul_service import Consul
from flask import Flask, request

# Flask app
app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)
args = parser.parse_args()

consul = Consul(args.port)
consul.register_service(
    service_name='logging-service',
    port=args.port,
    service_id=f"logging-{str(uuid.uuid4())}"
)

messages_map = consul.hazelcast_map()


@app.route("/logging", methods=['GET', 'POST'])
def logging():
    msg = ''

    if request.method == 'POST':
        _uuid = str(request.form["uuid"])
        msg = str(request.form["msg"])
        print('------', msg)
        print(f'Logging Service: [uuid: {_uuid}, msg: {msg}]')

        messages_map.lock(_uuid)
        try:
            messages_map.put(_uuid, msg)
        finally:
            messages_map.unlock(_uuid)

    elif request.method == 'GET':
        msg = ",".join(list(messages_map.values()))

    return msg


if __name__ == "__main__":
    app.run(host='localhost', port=args.port)
