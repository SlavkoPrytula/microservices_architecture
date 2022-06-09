import argparse
import consul

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)
args = parser.parse_args()

consul = consul.Consul(host='localhost', port=8500)


def test_kv():
    consul.kv.put('foo1', '1')
    consul.kv.put('foo2', '2')
    consul.kv.put('foo3', '3')


if __name__ == '__main__':
    test_kv()
