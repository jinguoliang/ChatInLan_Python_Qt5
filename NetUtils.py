import socket


def get_my_lan_ip():
    hostname = socket.gethostname()
    hosts = socket.gethostbyname_ex(hostname)[2]
    ip_by_hostname = [ip for ip in hosts if not ip.startswith("127.")]

    socks = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
    ip_by_sock = [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in socks]

    ip = ip_by_hostname or [ip_by_sock[0][1]]

    final_ip = (ip + ["no IP found"])[0]

    return final_ip


if __name__ == '__main__':
    print(get_my_lan_ip())
