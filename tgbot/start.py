from telethon import TelegramClient, sync
import socks
import socket
import requests
import urllib3
api_id = 563429
api_hash = '84297edbc5235720e01ddb6583aeca79'

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr='191.101.148.67', port='65234', username='osafon19', password='G1r0DvR')
socket.socket = socks.socksocket

print('hello')

client = TelegramClient(session='sesion_name.session', api_id=api_id, api_hash=api_hash, timeout=5, request_retries=1, connection_retries=1)
client.start()

