

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg
    


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)


        with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)
        
        ###################################################################
        # Receive who will start first from the server
        #1) 서버가 보내주는 선공 결과 받기
        data = client_socket.recv(SIZE).decode()
        print("FirstMover result From Server: {}".format(data))
        #2) 받은 결과를 분석하기
        firstmover = None # 선공 결과 저장할 변수 초기화
        # 줄 별로 잘라서 리스트 만들기
        for line in data.split('\r\n'):
            #'First-Move'로 시작하는 부분을 ':'로 잘라서
            if line.startswith('First-Move'):
                # :의 뒤([1])의 내용을 가져와서 firstmover에 저장
                firstmover = line.split(':')[1].strip()
                break
    
    
        ######################### Fill Out ################################
        # Send ACK 
        
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        
