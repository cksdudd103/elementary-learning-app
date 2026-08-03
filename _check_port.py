import socket, time
for _ in range(3):
    s = socket.socket()
    r = s.connect_ex(('127.0.0.1', 5000))
    print('connect_ex:', r)
    s.close()
    time.sleep(0.5)
