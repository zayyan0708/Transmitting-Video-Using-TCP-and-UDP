import cv2, imutils, socket
import numpy as np
import time
import base64  # we will use base64 to convert image data into text format


def TCP_client():
    BUFF_SIZE = 65536

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    x1 = time.time()
    client_socket.connect(('192.168.0.102', 5000))
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip = '192.168.0.102'  # socket.gethostbyname(host_name)
    print(host_ip)
    port = 5000
    message = b'Hello'
    c = 0
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    while True:
        packet, _ = client_socket.recvfrom(BUFF_SIZE)
        if c == 0:
            x2 = time.time()
            c += 1
        data = base64.b64decode(packet, ' /')
        npdata = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(npdata, 1)
        frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_socket.close()
            t = x2 - x1
            file = open('TCP_time.txt', 'w')
            file.write("TCP time: " + str(t))
            print("Time ", t)
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1


def UDP_client():

    BUFF_SIZE = 65536

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip = '192.168.0.102'  # socket.gethostbyname(host_name)
    print(host_ip)
    port = 9999
    message = b'Hello'
    c = 0

    x1 = time.time()
    client_socket.sendto(message, (host_ip, port))
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    while True:
        packet, _ = client_socket.recvfrom(BUFF_SIZE)
        x2 = time.time()
        t = x2 - x1
        if c == 0:
            file = open('UDP_time.txt', 'w')
            file.write("UDP time: " + str(t))
            print("Time ", t)
            c += 1
        data = base64.b64decode(packet, ' /')
        npdata = np.fromstring(data, dtype=np.uint8)
        frame = cv2.imdecode(npdata, 1)
        frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1


# main code

ch = True

while ch == True:

    val = input("1. TCP_Client\n2. UDP_Client\n3. Quit\nEnter your choice: ")

    if val == "1":

        TCP_client()

    elif val == "2":

        UDP_client()

    elif val == "3":

        print("Thank you!")

        ch = False

    else:

        print("wrong choice entered!!")
