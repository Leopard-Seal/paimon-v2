import socket
from urllib.parse import urlparse


def get_ip_port_from_url(url):
    # URLの解析
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port

    # デフォルトポートの設定（httpやhttpsの場合）
    if port is None:
        if parsed_url.scheme == "http":
            port = 80
        elif parsed_url.scheme == "https":
            port = 443

    # IPアドレスの取得
    ip_address = socket.gethostbyname(hostname)

    return ip_address, port


# 例：使用例
url = "https://edu3.te.kumamoto-nct.ac.jp/~te20fukuda"
ip, port = get_ip_port_from_url(url)
print("IP Address:", ip)
print("Port:", port)
