import cv2, imutils, socket
import numpy as np
import time
import base64  # we will use base64 to convert image data into text format


def TCP_Server():
    # assign buffer size
    BUFF_SIZE = 65536
    # make TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 5000))
    server_socket.listen(5)
    # for cross platform development we use set socket function with specified buff size
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    # take the host ip address
    host_ip = '192.168.0.105'
    print(host_ip)
    port = 5000
    # with port and ip we will make the socket address
    socket_address = (host_ip, port)
    print('Listening at:', socket_address)

    # capture the WebCam data
    vid = cv2.VideoCapture(0)  # 0 for webcam
    # variables to obtain the frame rate
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)

    client_socket = None
    while True:
        # server will try to accept from any client in its socket address
        if client_socket is None:
            client_socket, client_addr = server_socket.accept()
            print('GOT connection from ', client_addr)

        # width 400 becaause we want to send image in a single datagram
        WIDTH = 400

        while vid.isOpened():
            _, frame = vid.read()
            # resizing of image
            frame = imutils.resize(frame, width=WIDTH)
            # encode the image with jpeg quality of 80% ideal trade of image size and quality
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            # base64 encoding and decoding is used to convert binarydata to information interchange text format
            message = base64.b64encode(buffer)
            # send message to client address
            client_socket.sendto(message, client_addr)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # using imshow we can display transmitted frame at server side
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                server_socket.close()
                client_socket.close()
                break
            # count time taken by 20 frames in seconds
            if cnt == frames_to_count:
                try:
                    # divide 20 by that time interval to obtain frames per second
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1


def UDP_Server():
    BUFF_SIZE = 65536
    # make UDP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # for cross platform development we use set socket function with specified buff size
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    # get to the host ip address
    host_ip = '192.168.0.105'  # socket.gethostbyname(host_name)
    print(host_ip)
    port = 9999
    # with port and ip we will make the socket address
    socket_address = (host_ip, port)
    # binding server with the socket address
    server_socket.bind(socket_address)

    print('Listening at:', socket_address)

    # Capture WebCam data
    vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
    # variables to obtain the frame rate
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)

    while True:
        # server will try to recieve the datagram from any client in its socket address
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ', client_addr)
        # width 400 because we want to send image in a single datagram
        WIDTH = 400
        while vid.isOpened():
            _, frame = vid.read()
            # resizing of image
            frame = imutils.resize(frame, width=WIDTH)
            # encode the image with jpeg quality of 80% ideal trade of image size and quality
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            # base64 encoding and decoding is used to convert binarydata to information intechange text format
            message = base64.b64encode(buffer)
            # send the message to client address
            server_socket.sendto(message, client_addr)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # using imshow we can display transmitted frame at server side
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                server_socket.close()
                break
            # count time taken by 20 frames in seconds
            if cnt == frames_to_count:
                try:
                    # divide 20 by that time interval to obtain frames per second
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1


# main
ch = True
while (ch == True):
    val = input("1. TCP_SERVER\n 2.UDP_SERVER\n 3. Quit\n Enter your choice: ")
    if (val == "1"):
        TCP_Server()
    elif (val == "2"):
        UDP_Server()
    elif (val == "3"):
        print("Thank you!")
        ch = False
    else:
        print("wrong choice entered!!")
