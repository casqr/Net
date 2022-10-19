import optparse
import socket
import time
from concurrent.futures import ThreadPoolExecutor
import threading
from functools import partial


# start the scanner def for the port instance
def scanner(hostt, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect((hostt, port))
        print(f'[+] {port}/tcp Open')

    except Exception as e:
        print(f'[-] {port}/tcp closed | Reason:{e}')

    finally:
        sock.close()


def perform_ip(machine, ports_n):
    result = []
    with ThreadPoolExecutor(max_workers=10) as thread:
        result = thread.map(partial(scanner, hostt=machine), ports_n)
    for i in result:
        print(i)

    for port in ports_n:
        thread = threading.Thread(target=scanner, args=(machine, port))
        thread.start()
        thread.join()


def perform_w(machine, ports_n):
    # resolve the host or domain name to its ip
    ip = socket.gethostbyname(machine)
    # with ThreadPoolExecutor(max_workers=10) as thread:
    # for port in ports_n:
    # values = [ip, port]
    # f = thread.submit(lambda p: scanner(*p), values)
    # print(f.result())
    for port in ports_n:  # create a thread for each of the ports
        thread = threading.Thread(target=scanner, args=(ip, port))
        thread.start()


def main():
    # get the input of the host and the ports we want to scan
    parser = optparse.OptionParser('portScanner ' + '-H <Host Domain(website)> -P <Port> -I <Ip of the host if known>')
    parser.add_option('-H', dest='host', type='string', help='specify host domain')
    parser.add_option('-I', dest='ip', type='string', help='specify host ip')
    parser.add_option('-P', dest='port', type='string', help='specify port[s] separated by comma')
    (options, args) = parser.parse_args()
    # get the host and the ports from the shell
    host = options.host
    ip = options.ip
    ports = list(map(int, str(options.port).split(',')))

    if (host is None) | (ports[0] is None) and ip is None:
        print(parser.usage)
        exit(0)
    if host:
        try:
            start = time.perf_counter()
            perform_w(host, ports)
            end = time.perf_counter() - start
            print(end)

        except:
            print("[-] Cannot resolve '%s': Unknown host" % host)
            return
    else:
        perform_ip(ip, ports_n=ports)


if __name__ == '__main__':
    main()
