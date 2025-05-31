import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg


if __name__ == '__main__':

    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'

    while True:
        client_socket, client_addr = server_socket.accept()

        start = random.randrange(0,2)   # 서버가 0 또는 1을 랜덤하게 선택하여 시작하는 플레이어를 결정.
        # Protocol: Server decides who starts the game
        # ↓
        # start 값에 따라 누가 먼저 시작할지 결정
        # ↓  
        # ETTTP 프로토콜 메시지로 변환
        # ↓
        # 클라이언트에게 전송

        # start = 0 이면 서버가 먼저 시작. 즉 First Player가 Server
        # start = 1 이면 클라이언트가 먼저 시작. 즉 First Player가 Client
        print('Connected to client:', client_addr)

        ###################################################################
        # Send start move information to peer
        if start == 1:
            first_move = 'YOU'  # 클라이언트가 먼저 시작
        else:
            first_move = 'ME'   # 서버가 먼저 시작

        message = f"SEND ETTTP/1.0\r\n"           # SEND : 전송 / 1.0 버전의 ETTTP 프로토콜 / \r\n Carrage Return & 줄바꿈
        message += f"Host: {client_addr[0]}\r\n"  # Host 헤더 : 클라이언트의 IP 주소 (메시지를 받을 클라이언트의 IP 주소)
        message += f"Port: {client_addr[1]}\r\n"  # Port 헤더 : 클라이언트의 포트 번호 (메시지를 받을 클라이언트의 포트 번호)
        message += f"First-Move: {first_move}\r\n"# First-Move 헤더 : 누가 먼저 시작하는지에 대한 정보 
                                                  # (서버가 먼저 시작하는 경우 : 'I(Server) am First Player. YOU(Client) are Second Player.' )
                                                  # (클라이언트가 먼저 시작하는 경우 : 'YOU(Client) are First Player. I(Server) am Second Player.')
        message += f"\r\n"                        # 메시지 끝. 이게 없으면 메시지 파싱이 안됨.

        client_socket.sendall(message.encode('utf-8'))  # 클라이언트에게 메시지 전송
        print(f"[Server] First-move 메시지 전송:\n{first_move}")

        ###################################################################




        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game

        # 클라이언트로부터 ACK 수신 (타임아웃 설정)
        client_socket.settimeout(10)                           # 10초 타임아웃
        ack_message = client_socket.recv(SIZE).decode('utf-8') # SIZE = 1024
        client_socket.settimeout(None)                         # 타임아웃 해제

        print(f"[Server] ACK 수신: {ack_message[:20]}...")      # initial 20 characters 출력

        # check_msg 함수로 ACK 메시지 검증하기
        if check_msg(ack_message, MY_IP):
            # ACK 메시지에서 First-Move 값 추출하여 확인
            lines = ack_message.split('\r\n')                  # 메시지를 줄 단위로 분리
            received_first_move = None

            for line in lines: # 줄 별로 분리한 ACK 메시지에서,
                if line.startswith('First-Move:'): # 'First-Move:'로 시작하는 줄을 찾음
                    # 'First-Move:' 다음에 오는 값을 추출
                    received_first_move = line.split(':', 1)[1].strip()
                    break
        ###################################################################
        # [ Server와 클라이언트 간의 ACK 메시지 검증 (이전 버전) ]
        #   if received_first_move == first_move:
        #       print(f"[서버] ACK 검증 성공! 게임 시작")
        #   else:
        #       print(f"[서버] ACK 값 불일치: 전송={first_move}, 수신={received_first_move}")
        #       client_socket.close()
        #       continue
        ###################################################################
        # 서버랑 클라이언트랑 ACK를 주고받는 과정에서 의도해석 오류가 생겨버림
        # [ Client 부분 ]
        # if firstmover == "YOU":
        #       mymove = "ME"    # 서버가 "YOU"라고 하면 클라이언트는 "ME"
        #       start = 1
        #   else:
        #       mymove = "YOU"   # 서버가 "ME"라고 하면 클라이언트는 "YOU"
        #       start = 0
        # [ Server 부분 ]
        # if start == 1:    # 클라이언트가 먼저 시작하는 경우
        #     first_move = 'YOU'  # 클라이언트가 먼저 시작
        # else:
        #     first_move = 'ME'   # 서버가 먼저 시작
        #
        # 이렇게 되면 클라이언트는 "ME"라고 하고 서버는 "YOU"라고 하게 되어 서로 의도해석 오류가 생김
        # 따라서, 클라이언트와 서버가 서로 의도해석 오류가 생기지 않도록 해야함
        ###################################################################
        if first_move == "ME":
            # 내가 먼저라고 했으니까 상대는 YOU라고 해야함
            if received_first_move == "YOU":
                # "ACK 확인, 서버 먼저 시작
                ack_ok = True
            else:
                # "ACK 틀림! 서버가 ME라고 했는데 Client는 ", received_first_move, "라고 함
                ack_ok = False
        elif first_move == "YOU":
            # Server가 '너 먼저 해'라고 했으니 Clinet는 ME라고 해야함  
            if received_first_move == "ME":
                # "ACK 맞음! 클라이언트가 먼저 시작
                ack_ok = True
            else:
                #"ACK 틀림! 서버가 YOU라고 했는데 상대가", received_first_move, "라고 함
                ack_ok = False
        else:
            print("first_move 오류 확인 필요:", first_move)
            ack_ok = False

        if ack_ok == True:
            # ACK가 맞으면 게임 시작 가능
            print("ACK 확인, 게임 시작 가능")
        else:
            print("게임 시작 불가능! ACK 검증 오류")
            client_socket.close()
            continue 


        ###################################################################

        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()

        client_socket.close()
        print('[Server] Game over. Client disconnected.')

        break
    server_socket.close()
    print('[Server] Server socket closed.')

