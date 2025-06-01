
import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-01-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"YOU"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"ME"}   
        else:
            self.myID = 0
            self.title('34743-01-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        # 소켓을 통해 메세지 가져오기
        msg =  self.socket.recv(SIZE).decode()
        print("Get message\n {}".format(msg))
        
        msg_valid_check = check_msg(msg, self.recv_ip)
       
        # Message is not valid -> 소켓 닫고 종료
        # (250531) [우림 수정] True 반환하면 유효한거 아닌가..? not valid면 False 반환해야함
        if not msg_valid_check:
            print("check_msg()가 False 반환, 프로그램 종료")
            self.socket.close()
            self.quit()
            return
        else:  # If message is valid - send ack, update board and change turn
            # 메세지에서 어디로 move할지를 찾아서 move_where에 저장
            move_where = None
            # 라인을 들여쓰기로 분리
            for line in msg.split('\r\n'):
                # New-Move 뒤에 있을 move 좌표를 저장
                if line.startswith('New-Move:'):
                    move_where = line
                    break
            # 좌표값을 string에 저장하고, 이를 tuple로 바꿈 (계산을 위해!)
            move_change = move_where.split(':')[1].strip()
            row, col = eval(move_change)
            
            # 3*3보드에게 번호를 매핑. 0~8
            # 2차원을 1차원으로 바꿔 번호를 매기는 row*n +col 공식을 참고함
            loc = row * 3 + col

            # 완료한 후 ACK 보내기
            ack_msg = "ACK ETTTP/1.0\r\nHost: {}\r\nNew-Move: ({}, {})\r\n\r\n".format(self.send_ip, row, col)
            # 메세지 보냄
            self.socket.sendall(ack_msg.encode())

            
            ######################################################   
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self): # 텍스트박스 쓸 경우 (turn 고려 필요)
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        

        # =================================================================
        # [ 1단계: 메시지에서 New-Move 좌표 정보 추출 및 초기화 ]
        # =================================================================

        # d_msg에서 New-Move: (row, col) 부분을 찾아서 좌표를 계산
        # 좌표를 계산해서 debug_move_where에 저장
        debug_move_where = None        # 0~8 사이의 보드 위치 (1차원 배열 인덱스)
        debug_move_where_coord = None  # "(row, col)" 형태의 원본 좌표 문자열
        drow = None                    # 행 좌표 (0~2)
        dcol = None                    # 열 좌표 (0~2)

        # =================================================================
        # [ 2단계: 메시지 파싱하여 New-Move 좌표 추출 ]
        # =================================================================

        # 줄바꿈으로 메시지를 나눔 (네트워크 프로토콜에서는 \r\n으로 줄 구분)
        lines = d_msg.split('\r\n')     # ['Header1: value1', 'Header2: value2', 'New-Move: (1, 2)', ...]

        # 줄바꿈으로 나눈 메시지에서 New-Move: 부분을 찾아서 좌표를 계산
        for line in lines:              # 각 줄을 순회하면서
            if line.startswith('New-Move:'):    # 'New-Move:'로 시작하는 줄을 찾음
                # 만약 'New-Move: (1, 2)' 라면, -> '(1, 2)' 추출
                debug_move_where_coord = line.split(':')[1].strip()  # ':'로 분리 후 두 번째 부분, 공백 제거
                
                # '(1, 2)' 문자열을 실제 정수 좌표로 변환 (eval 사용)
                drow, dcol = eval(debug_move_where_coord)  # eval("(1, 2)") -> (1, 2) 튜플
                
                # 2차원 좌표(row, col)를 1차원 배열 인덱스로 변환
                # 3x3 보드에서 (row, col) -> row*3 + col
                # 예: (0,0)->0, (0,1)->1, (0,2)->2, (1,0)->3, (1,1)->4, ...
                debug_move_where = drow * 3 + dcol
                break                           # 찾았으므로 반복문 종료

        # =================================================================
        # [ 3단계: 좌표 추출 성공 여부 검증 ]
        # =================================================================

        if debug_move_where_coord is None:      # New-Move: 헤더와 이를 통해 추출한 좌표를 찾지 못한 경우
            print("좌표 찾을 수 없음")
            return                              # 함수 종료

        if drow is None or dcol is None:        # eval() 실행 실패 또는 좌표 파싱 실패
            print("row or col -> None")
            return                              # 함수 종료

        # =================================================================
        # [ 4단계: 좌표 범위 유효성 검사 ]
        # =================================================================
            
        if drow < 0 or drow > 2:               # 행 좌표가 0~2 범위를 벗어난 경우
            print("row 범위 오류")               # 3x3 보드에서 유효하지 않은 행
            return                              # 함수 종료

        if dcol < 0 or dcol > 2:               # 열 좌표가 0~2 범위를 벗어난 경우  
            print("col 범위 오류")               # 3x3 보드에서 유효하지 않은 열
            return                              # 함수 종료
            
        if debug_move_where < 0 or debug_move_where > 8:  # 1차원 인덱스가 0~8 범위를 벗어난 경우
            print("잘못된 위치")                 # 3x3=9개 칸에서 유효하지 않은 위치
            return                              # 함수 종료

        # =================================================================
        # [ 5단계: 게임 보드에서 해당 위치 사용 가능 여부 확인 ]
        # =================================================================

        # 이미 선택된 위치인지 확인 (보드 값이 0이 아니면 이미 사용됨)
        # self.board[i] == 0: 빈 칸, != 0: 이미 X 또는 O가 놓여진 칸
        if self.board[debug_move_where] != 0:
            print("이미 선택된 위치")            # 중복 수 방지
            return                              # 함수 종료


        # =================================================================
        # [ 6단계: 피어(상대방)에게 메시지 전송 ]
        # =================================================================

        '''
        Send message to peer
        상대방에게 내 수를 알리는 메시지 전송
        '''

        # 소켓을 통해 d_msg를 상대방에게 전송
        self.socket.sendall(d_msg.encode())     # 문자열을 바이트로 인코딩하여 전송
        print("메시지 전송 완료")                # 전송 완료 확인 로그

        # =================================================================
        # [ 7단계: 상대방으로부터 ACK(응답 확인) 메시지 수신 ]
        # =================================================================

        '''
        Get ack
        상대방의 응답(ACK) 메시지 받기
        '''

        # 상대방으로부터 ACK 메시지 수신 (SIZE = 1024 바이트)
        ack_msg = self.socket.recv(SIZE).decode()   # 바이트를 문자열로 디코딩
        print("ACK 받음:", ack_msg[:10], "...")     # ACK 메시지의 처음 10글자만 출력 (로그 길이 제한)

        # =================================================================
        # [ 8단계: 수신한 ACK 메시지 형식 검증 ]
        # =================================================================

        # check_msg 함수로 ACK 메시지의 형식과 발신자 IP 확인
        if not check_msg(ack_msg, self.recv_ip):   # 메시지 형식이 올바르지 않거나 IP가 일치하지 않는 경우
            print("ACK 형식 오류")                  # 프로토콜 위반 또는 잘못된 발신자
            return                                  # 함수 종료

        # =================================================================
        # [ 9단계: 최종 처리 - 검증된 위치 정보를 loc 변수에 저장 ]
        # =================================================================

        loc = debug_move_where                      # 모든 검증을 통과한 유효한 위치를 loc에 저장
                                                # 이후 게임 로직에서 사용할 최종 위치 정보

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        # 3*3 보드에서 좌표계산
        row,col = divmod(selection,3)
        
        ###################  Fill Out  #######################

        # send message and check ACK
        ack_msg = "SEND ETTTP/1.0\r\nHost: {}\r\nNew-Move: ({}, {})\r\n\r\n".format(self.send_ip, row, col)
        # 메세지 보냄
        self.socket.sendall(ack_msg.encode())
        
        # 상대가 잘 받았는지에 대한 ACK 받기
        your_ack = self.socket.recv(SIZE).decode()
        print("Your ACK received:\n{}".format(your_ack))
        
        # 에러가 있을 경우 False 반환
         # (250531) [우림 수정] True 반환하면 유효한거 아닌가..? not valid면 False 반환해야함
        if not check_msg(your_ack, self.recv_ip):
            print("ACK received Failed")
            return False
        
        # ACK에 이상이 없으면 true
        return True
        ######################################################  

    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        # ETTTP 프로토콜에 맞게 내가 보낼 메세지 작성
        my_msg = "RESULT ETTTP/1.0\r\nHost: {}\r\nWinner: {}\r\n\r\n".format(self.send_ip, winner)
        
        # get : true 이면 -> 상대 유저가 winner, 상대가 먼저 결과 보냄
        if get == True:
            # 상대 메세지 받고
            your_msg = self.socket.recv(SIZE).decode()
            print("상대 결과:", your_msg.strip())
            # 내 결과 보내기
            self.socket.sendall(my_msg.encode())
            print("내 결과:", my_msg.strip())
        
        # get : false 이면 -> 이 유저가 winner, 먼저 결과 보냄
        else :
            # 내 메세지 먼저 보내고
            self.socket.sendall(my_msg.encode())
            print("내 결과:", my_msg.strip())
            # 상대 메세지 받기
            your_msg = self.socket.recv(SIZE).decode()
            print("상대 결과:", your_msg.strip())
            
        # check_msg() 함수 써서 ETTTP 맞는 지 확인
        if check_msg(your_msg, self.recv_ip) == False:
            print("상대의 메세지 형식 오류")
            return False
        
        your_winner = None
        # 상대 메시지의 winner부분 자르기
        for line in your_msg.strip().split('\r\n'):
            if line.startswith('Winner:'):
                # Winner 뒤에 내용을 변수 your_winner에 저장
                your_winner = line.split(':', 1)[1].strip()
                break
        
        # 내 winner와 상대의 your_winner 변수 비교
        # (250601) 승자가 정해지고 나서 게임이 끝나도 Somethings wrong... 이 뜨는 문제 해결
        # 기존 코드에서는 양쪽에서 같은 결과를 보냈음
        # e.g. Server가 이겼을 때, 'YOU'라고 보내고(?), Client는 상대방이 이겼으니 'YOU'라고 보내는 경우가 있었음
        # 기존 코드 
        # if (winner == "ME" and your_winner == "YOU")or (winner == "YOU" and your_winner == "ME"):
        if winner == your_winner or (winner == "ME" and your_winner == "YOU") or (winner == "YOU" and your_winner == "ME"):
            return True
        else:
            print("상대와 나의 winner 결과 다름, 나: {}, 상대: {}".format(winner, your_winner))
        return False
            
        

        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    # ETTTP format인지 확인하기 -> 메세지를 줄대로 자르고, 각각 있는지 확인
    linelist = msg.strip().split('\r\n')
    
    # ETTTP/1.0 확인
    if len(linelist) == 0 or 'ETTTP/1.0' not in linelist[0]:
        print("ETTTP 불일치 : 형식 오류")
        return False
    
    # Host 확인
    correctIP = False
    for line in linelist:
        # Host : 뒤의 내용을 check
        if line.startswith('Host:'):
            IP = line.split(':', 1)[1].strip()
            if IP == recv_ip:
                correctIP = True
    if correctIP == False:
        print("ETTTP 불일치 : IP 오류")
        return False
    
    # First-Move, New-Move, Winner 중 하나라도 있으면 OK
    has_info = False
    for line in linelist:
        if line.startswith('First-Move') or line.startswith('New-Move') or line.startswith('Winner'):
            has_info = True
            break
    if not has_info:
        print("ETTTP 불일치 : 필요 정보 오류")
        return False
    
    return True
    

    ######################################################  
