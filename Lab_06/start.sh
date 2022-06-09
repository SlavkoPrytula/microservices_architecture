docker run \
    -d \
    -p 8500:8500 \
    -p 8600:8600/udp \
    --name=bert consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

python setup.py
