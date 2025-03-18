import random, time
from websocket import create_connection
ws = create_connection("ws://verbal-sleep.picoctf.net:60291/ws/")

score = -17
while score > -99999:
    ws.send(f"eval {score}")
    result =  ws.recv()
    print(result)
    score -= random.randint(-20, 10000)
    time.sleep(0.1)

prompts = ["eval -9999", "mate -3", "mate -2", "mate -1", "mate 0"]
for p in prompts:
    ws.send(p)
    print(ws.recv())

ws.close()
