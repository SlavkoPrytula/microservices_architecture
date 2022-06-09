# make sure to have no docker image running
bash start.sh

python ./tests/consul_test.py --port=8500