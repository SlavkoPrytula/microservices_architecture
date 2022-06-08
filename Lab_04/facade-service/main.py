import random
from flask import Flask, request
import requests
import uuid
import json

app = Flask(__name__)

logging_services = ["http://localhost:8083/logging_service",
                    "http://localhost:8084/logging_service",
                    "http://localhost:8085/logging_service"]

message_services = ["http://localhost:8081/message_service",
                    "http://localhost:8082/message_service"]


@app.route('/facade_service', methods=['GET'])
def get_data():
    logging_service = random.choice(logging_services)
    message_service = random.choice(message_services)

    logging_service_data = requests.get(logging_service).text
    message_service_data = requests.get(message_service).text
    data = f'{logging_service_data}: {message_service_data}'

    return data


@app.route('/facade_service', methods=['POST'])
def post_message():
    message = request.get_json()
    message_uuid = str(uuid.uuid4())

    data = {
        "message": message,
        "message_uuid": message_uuid
    }

    logging_service = random.choice(logging_services)
    messages_service = random.choice(message_services)

    response_logging = requests.post(url=logging_service,
                                     data=json.dumps(data),
                                     headers={"Content-Type": "application/json"}
                                     )
    response_messages = requests.post(url=messages_service,
                                      data=json.dumps(data),
                                      headers={"Content-Type": "application/json"}
                                      )

    return {
        "statusCode logging service": response_logging.status_code,
        "statusCode message service": response_messages.status_code,
    }


if __name__ == '__main__':
    app.run(port=8080)


