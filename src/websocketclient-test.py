from PyLibs.websocketclient import WebsocketClient

client = WebsocketClient('ws://localhost:8765/')
client.start()
print("Post start")
client.write("Hello world")
print("post write")
