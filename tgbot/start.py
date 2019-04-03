from telethon import TelegramClient, sync
import socks
import socket
import requests
import urllib3
api_id = 
api_hash = ''

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr='', port='', username='', password='')
socket.socket = socks.socksocket

print('hello')

client = TelegramClient(session='sesion_name.session', api_id=api_id, api_hash=api_hash, timeout=5, request_retries=1, connection_retries=1)
client.start()

