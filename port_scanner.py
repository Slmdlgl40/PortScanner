import socket
import argparse
import threading
from termcolor import colored

class PortScanner():

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="port_scanner",description="Scans the ports simply",epilog="python port_scanner <target_ip> -p <number of ports>")
        self.parser.add_argument("host", type=str, help="Enter the hostname")
        self.parser.add_argument("-p", "--port", type=int,default=1000, help="Number of ports")
        self.args = self.parser.parse_args()
        self.host, self.max_port = self.args.host, self.args.port

    def conn_scan(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #try bloğu içinde tanımlayınca finally kısmında görmeyebiliyor
        try:
            sock.connect((host, port))
            print(colored("Open port:{}".format(port), "blue",attrs=["dark"]))
            self.get_banner(host, port)
        except:
            pass
        finally:
            sock.close()

    def get_banner(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
            banner = sock.recv(1024).decode()
            print(colored("Found service of port {}:{}".format(port, banner), "magenta"))
        except:
            pass
        finally:
            sock.close()

    def start_scan(self):
        try:
            ip = socket.gethostbyname(self.host)
        except:
            print("Unknown host {}".format(self.host))
        try:
            name = socket.gethostbyaddr(ip)
            print("Scan result for " + name[0])
        except:
            print("Scan result for " + ip)

        socket.setdefaulttimeout(1)

        for target in range(1,self.max_port + 1):
            t = threading.Thread(target=self.conn_scan, args=(ip, target))
            t.start()

port_scanner = PortScanner()
port_scanner.start_scan()