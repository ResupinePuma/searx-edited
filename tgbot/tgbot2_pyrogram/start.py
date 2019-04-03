from pyrogram import Client
import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr='191.101.148.67', port='65234', username='osafon19', password='G1r0DvR')
socket.socket = socks.socksocket

app = Client(
    "my_account",
    api_id=563429,
    api_hash="84297edbc5235720e01ddb6583aeca79"
)


