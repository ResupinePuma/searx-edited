from telethon import TelegramClient, sync
import socks
import socket
api_id = 563429
api_hash = '84297edbc5235720e01ddb6583aeca79'

proxy = socks.socksocket()
proxy.set_proxy(socks.PROXY_TYPE_SOCKS5, addr='76.98.94.54 ', port='35753')

#socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, '94.177.252.200', port=8080)
#socket.socket = socks.socksocket

print('hello')

client = TelegramClient(session='sesion-name.session', api_id=api_id, api_hash=api_hash, proxy=proxy, timeout=5, request_retries=1, connection_retries=1)
client.start()

me = client.get_me()
print(me.stringify())