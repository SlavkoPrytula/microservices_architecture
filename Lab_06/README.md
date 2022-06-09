# **Lab 05: Microservices with Consul**

**Author: Yaroslav Prytula**

----

##### Table of Content
- [Requirement](#requirement)
- [Idea](#idea)
- [Usage](#usage)
  - [Start Consul](#start_consul)
  - [Start Hazelcast](#start_hazelcast)
  - [Run](#run)
  - [Requests](#requests)
- [Results](#results)
- [References](#references)


----

<a name="requirement"></a>
## **Requirement**


Before starting to work with current repository please make sure to download it locally on your machine

```bash
git clone https://github.com/SlavkoPrytula/microservices_architecture/
git fetch
git checkout micro_consul
```

Install the requirements

```bash
pip install -r requirements.txt
```

----

<a name="usage"></a>
## **Usage**

<a name="start_consul"></a>
#### Docker Run | Starting Consul

```bash
bash start.sh
```

#### Optional [Testing Consul]

```bash
bash test_consul.sh
```

<a name="start_hazelcast"></a>
#### Start Hazelcast 

For more information and further tutorial refer to the [original page](https://hazelcast.org/imdg/get-started/)

Start Hazelcast **3** clusters locally

```bash
# x3 times
cd hazelcast-4.2.5/bin
bash start.sh
```

You can also download the hazelcast client locally and start it

```bash
hz-start
```

- This will create one node in the distributed system

<br />

<a name="run"></a>
#### Run 

Facade Service is running locally on the **8080** port
```bash
python facade-service/main.py --port=8080
```

Logging Service is running locally on the **8081, 8082, 8083** ports
```bash
python logging-service/main.py --port=8081
python logging-service/main.py --port=8082
python logging-service/main.py --port=8083
```

Messages Service is running locally on the **8084, 8085** ports
```bash
python logging-service/main.py --port=8084
python logging-service/main.py --port=8085
```

<br />

<a name="requests"></a>
#### Requests

In the main folder directory file `requests.http` stores the needed request commands `(POST/GET)`
You can also use Postman tool, curl...

----

<a name="results"></a>
## **Results**

For fully detailed usage and results please refer to the `Lab_05.pdf` file

----

<a name="references"></a>
## **References**
Good tutorial with code: https://github.com/hazelcast/hazelcast-python-client