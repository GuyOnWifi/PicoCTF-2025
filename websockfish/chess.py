import random, time
from websocket import create_connection
ws = create_connection("ws://verbal-sleep.picoctf.net:60291/ws/")

ws.send(f"eval -99999")
print(ws.recv())

"""
score = -17
while score > -99999:
    ws.send(f"eval {score}")
    result =  ws.recv()
    print(result)
    score -= random.randint(-20, 10000)
    time.sleep(0.1)
"""

ws.close()
