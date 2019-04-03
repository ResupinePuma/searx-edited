from pyrogram import Client
import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr='', port='', username='', password='')
socket.socket = socks.socksocket

app = Client(
    "my_account",
    api_id=,
    api_hash=""
)


