

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
            first_move = 'YOU(Client) are First Player. I(Server) am Second Player.'
        else: 
            first_move = 'I(Server) am First Player. YOU(Client) are Second Player.'
        first_move = 'START ' + first_move + '\n'
        client_socket.send(first_move.encode())

        message = f"SEND ETTTP/1.0\r\n"           # SEND : 전송 / 1.0 버전의 ETTTP 프로토콜 / \r\n Carrage Return & 줄바꿈
        message += f"Host: {client_addr[0]}\r\n"  # Host 헤더 : 클라이언트의 IP 주소 (메시지를 받을 클라이언트의 IP 주소)
        message += f"Port: {client_addr[1]}\r\n"  # Port 헤더 : 클라이언트의 포트 번호 (메시지를 받을 클라이언트의 포트 번호)
        message += f"First-Move: {first_move}\r\n"# First-Move 헤더 : 누가 먼저 시작하는지에 대한 정보 
                                                  # (서버가 먼저 시작하는 경우 : 'I(Server) am First Player. YOU(Client) are Second Player.' )
                                                  # (클라이언트가 먼저 시작하는 경우 : 'YOU(Client) are First Player. I(Server) am Second Player.')
        message += f"\r\n"                        # 메시지 끝. 이게 없으면 메시지 파싱이 안됨.
        send_header = check_msg(message)          # 메시지 파싱 확인
        if send_header is None:
            print('Error: Invalid message format.')
            client_socket.close()
            continue


        try:
            # 클라이언트에게 메시지 전송
            client_socket.send(message.encode('utf-8'))
            print(f"[Server] First-Move 메시지 전송: {first_move}")
        except Exception as e:
            print(f"[Server] First-Move 메시지 전송 실패: {e}")
            client_socket.close()
            continue


    ###################################################################




    ######################### Fill Out ################################
    # Receive ack - if ack is correct, start game

        try:
            # 클라이언트로부터 ACK 수신 (타임아웃 설정)
            client_socket.settimeout(10)  # 10초 타임아웃
            ack_message = client_socket.recv(SIZE).decode('utf-8') # SIZE = 1024
            if not ack_message:
                print("[Server] ACK 메시지가 비어 있습니다. 연결을 종료합니다.")
                client_socket.close()
                continue
            client_socket.settimeout(None)  # 타임아웃 해제

            print(f"[Server] ACK 수신: {ack_message[:20]}...")  # initial 20 characters 출력

            # check_msg 함수로 ACK 메시지 검증하기
            if check_msg(ack_message, MY_IP):
                # ACK 메시지에서 First-Move 값 추출하여 확인
                lines = ack_message.split('\r\n') # 메시지를 줄 단위로 분리
                received_first_move = None
                
                for line in lines: # 줄 별로 분리한 ACK 메시지에서,
                    if line.startswith('First-Move:'): # 'First-Move:'로 시작하는 줄을 찾음
                        # 'First-Move:' 다음에 오는 값을 추출
                        received_first_move = line.split(':', 1)[1].strip()
                        break
                
                # 전송한 값과 수신한 값이 일치하는지 확인
                if received_first_move == first_move:
                    print(f"[서버] ACK 검증 성공! 게임 시작")
                else:
                    print(f"[서버] ACK 값 불일치: 전송={first_move}, 수신={received_first_move}")
                    client_socket.close()
                    continue
            else:
                print(f"[Server] 유효하지 않은 ACK 메시지")
                client_socket.close()
                continue
                
        except socket.timeout:
            print(f"[Server] ACK 수신 Time-out 발생")
            client_socket.close()
            continue
        except Exception as e:
            print(f"[Server] ACK 수신 실패: {e}")
            client_socket.close()
            continue

    ###################################################################


        recv_header = client_socket.recv(SIZE).decode()
        print('Received header from client:', recv_header.strip())      
    ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        print('[Server] Game over. Client disconnected.')
        
        break
    server_socket.close()
    print('[Server] Server socket closed.')
    