# 📡 ETTTP 프로토콜 명세서
**이화 틱택토 프로토콜 v1.0**

## 📋 개요

ETTTP (Ewha Tic-Tac-Toe Protocol)는 TCP 연결을 통한 실시간 멀티플레이어 틱택토 게임을 위해 설계된 커스텀 애플리케이션 계층 프로토콜입니다. 이 프로토콜은 동기화된 게임플레이, 움직임 검증, 그리고 피어 간 결과 검증을 보장합니다.

## 🏗️ 프로토콜 아키텍처

### 통신 모델
```
클라이언트 ←→ TCP 소켓 ←→ 서버
   ↓          ETTTP          ↓
게임 상태 ←→ 프로토콜 ←→ 게임 상태
```

### 메시지 플로우
```
1. TCP 연결 설정
2. 초기 설정 (서버 → 클라이언트)
3. 게임 루프 (양방향)
   ├── 움직임 메시지 (SEND)
   ├── 확인 응답 (ACK)
   └── 상태 동기화
4. 결과 검증 (양방향)
5. 연결 종료
```

## 📨 메시지 형식 명세

### 일반 메시지 구조
```
<명령어> ETTTP/1.0 \r\n
<헤더-필드>: <값> \r\n
[추가 헤더들...]
\r\n
[메시지 본문]
```

### 필수 요소
- **프로토콜 버전**: 항상 `ETTTP/1.0`
- **줄 종료**: `\r\n` (CRLF)
- **헤더 종료**: 빈 줄(`\r\n`)
- **문자 인코딩**: UTF-8

### 헤더 필드
| 필드명 | 필수여부 | 설명 | 예시 |
|------------|----------|-------------|---------|
| Host | 예 | 상대방 IP 주소 | `127.0.0.1` |
| New-Move | 상황별 | 움직임 좌표 | `(1, 2)` |
| First-Move | 상황별 | 초기 턴 배정 | `YOU` 또는 `ME` |
| Winner | 상황별 | 게임 결과 | `ME`, `YOU`, `DRAW` |

## 🎮 메시지 유형

### 1. 초기 설정 메시지

#### 목적
서버가 무작위로 첫 번째 플레이어를 결정하고 클라이언트에게 알림.

#### 형식
```
SEND ETTTP/1.0 \r\n
Host: <클라이언트_IP> \r\n
First-Move: <배정> \r\n
\r\n
```

#### 매개변수
- **클라이언트_IP**: 클라이언트의 IP 주소
- **배정**: 
  - `YOU` - 클라이언트가 먼저 움직임 (X)
  - `ME` - 서버가 먼저 움직임 (X)

#### 예시
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
First-Move: YOU \r\n
\r\n
```

#### 응답
클라이언트는 ACK 메시지로 응답해야 함:
```
ACK ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
First-Move: YOU \r\n
\r\n
```

### 2. 게임 움직임 메시지

#### 목적
플레이어의 움직임을 상대방에게 알려 보드 동기화.

#### 형식
```
SEND ETTTP/1.0 \r\n
Host: <상대방_IP> \r\n
New-Move: (<행>, <열>) \r\n
\r\n
```

#### 매개변수
- **상대방_IP**: 메시지를 받을 상대방의 IP 주소
- **행**: 행 좌표 (0-2)
- **열**: 열 좌표 (0-2)

#### 좌표 시스템
```
(0,0) (0,1) (0,2)     보드 인덱스:
(1,0) (1,1) (1,2)  →   0  1  2
(2,0) (2,1) (2,2)      3  4  5
                       6  7  8
```

#### 예시
```
SEND ETTTP/1.0 \r\n
Host: 192.168.0.2 \r\n
New-Move: (1, 2) \r\n
\r\n
```

#### 응답
상대방은 ACK로 응답해야 함:
```
ACK ETTTP/1.0 \r\n
Host: 192.168.0.1 \r\n
New-Move: (1, 2) \r\n
\r\n
```

### 3. 확인 응답 메시지

#### 목적
상대방의 움직임을 받았고 검증했음을 확인.

#### 형식
```
ACK ETTTP/1.0 \r\n
Host: <발신자_IP> \r\n
New-Move: (<행>, <열>) \r\n
\r\n
```

#### 매개변수
- **발신자_IP**: 원래 발신자의 IP 주소
- **행, 열**: 받은 좌표를 그대로 에코

#### 검증 규칙
- 움직임 좌표가 경계 내에 있어야 함 (0-2)
- 대상 셀이 비어있어야 함
- 발신자의 유효한 턴이어야 함
- 메시지 형식이 올바라야 함

#### 에러 처리
ACK를 받지 못하거나 유효하지 않은 경우:
- 발신자는 메시지 실패로 간주
- 연결을 종료해야 함
- 게임이 에러 상태로 종료됨

### 4. 결과 검증 메시지

#### 목적
피어 간 게임 결과를 교차 검증하여 일관성 보장.

#### 형식
```
RESULT ETTTP/1.0 \r\n
Host: <상대방_IP> \r\n
Winner: <결과> \r\n
\r\n
```

#### 매개변수
- **상대방_IP**: 상대방의 IP 주소
- **결과**:
  - `ME` - 발신자가 게임에서 승리
  - `YOU` - 상대방이 게임에서 승리  
  - `DRAW` - 게임이 무승부로 종료

#### 예시 시나리오: 클라이언트 승리
**클라이언트가 보냄:**
```
RESULT ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
Winner: ME \r\n
\r\n
```

**서버가 보냄:**
```
RESULT ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
Winner: YOU \r\n
\r\n
```

#### 검증
- 양쪽 피어의 결과가 상보적이어야 함
- 한 피어의 `ME` = 다른 피어의 `YOU`
- `DRAW`는 양쪽 피어가 동의해야 함
- 일치하지 않는 결과는 동기화 에러를 나타냄

## 🔍 메시지 검증

### 파싱 규칙

#### 1. 형식 검증
```python
def validate_message_format(message):
    lines = message.split('\r\n')
    
    # 명령어 줄 확인
    command_line = lines[0]
    if not command_line.endswith(' ETTTP/1.0'):
        return False
    
    # 빈 줄 종료 확인
    if lines[-2] != '':
        return False
    
    return True
```

#### 2. 헤더 검증
```python
def parse_headers(message):
    lines = message.split('\r\n')
    headers = {}
    
    for line in lines[1:]:
        if line == '':  # 헤더 끝
            break
        if ':' not in line:
            return None
        
        key, value = line.split(':', 1)
        headers[key.strip()] = value.strip()
    
    return headers
```

#### 3. 좌표 검증
```python
def validate_coordinates(coord_str):
    # 예상 형식: "(행, 열)"
    import re
    pattern = r'\((\d+),\s*(\d+)\)'
    match = re.match(pattern, coord_str)
    
    if not match:
        return False
    
    row, col = int(match.group(1)), int(match.group(2))
    return 0 <= row <= 2 and 0 <= col <= 2
```

### 에러 조건

| 에러 유형 | 설명 | 행동 |
|------------|-------------|--------|
| 잘못된 메시지 | 유효하지 않은 ETTTP 형식 | 거부 및 연결 닫기 |
| 유효하지 않은 좌표 | 경계를 벗어난 움직임 | 거부 및 연결 닫기 |
| 잘못된 턴 | 상대방 턴에 움직임 | 거부 및 연결 닫기 |
| 점유된 셀 | 이미 점유된 위치로 움직임 | 거부 및 연결 닫기 |
| 누락된 헤더 | 필수 헤더 없음 | 거부 및 연결 닫기 |

## 🔄 프로토콜 상태 머신

### 연결 상태
```
연결해제됨 → 연결중 → 연결됨 → 게임설정 → 
플레이중 → 게임종료 → 연결해제됨
```

### 상태 전환

#### 연결중 → 연결됨
- TCP 소켓 설정됨
- 초기 설정 준비

#### 연결됨 → 게임설정  
- 서버가 First-Move 메시지 전송
- 클라이언트가 ACK로 응답

#### 게임설정 → 플레이중
- 양쪽 피어가 턴 순서 인지
- 게임 보드 초기화됨

#### 플레이중 → 플레이중
- 움직임 메시지 교환
- ACK 확인 수신
- 피어 간 턴 교대

#### 플레이중 → 게임종료
- 승리 조건 감지
- 결과 검증 시작

#### 게임종료 → 연결해제됨
- 결과 메시지 교환
- 연결 종료

### 메시지 순서도

```
클라이언트                서버
  |                     |
  |←-- TCP 연결 ---------|
  |                     |
  |← SEND First-Move ---|
  |                     |
  |-- ACK First-Move →--|
  |                     |
  |-- SEND New-Move -→--|  (클라이언트가 먼저인 경우)
  |                     |
  |←-- ACK New-Move ----|
  |                     |
  |←- SEND New-Move ----|  (서버 턴)
  |                     |
  |-- ACK New-Move --→--|
  |                     |
  |      ... 게임 계속 ...
  |                     |
  |-- RESULT Winner --→--|
  |                     |
  |←-- RESULT Winner ---|
  |                     |
  |-- TCP 닫기 -----→--|
```

## 🛠️ 구현 가이드라인

### 소켓 설정
```python
# 서버 설정
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 12000))
server_socket.listen(1)

# 클라이언트 설정  
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12000))
```

### 메시지 전송
```python
def send_etttp_message(socket, command, headers):
    message = f"{command} ETTTP/1.0\r\n"
    
    for key, value in headers.items():
        message += f"{key}: {value}\r\n"
    
    message += "\r\n"  # 빈 줄 종료
    
    try:
        socket.send(message.encode('utf-8'))
        return True
    except Exception as e:
        print(f"전송 에러: {e}")
        return False
```

### 메시지 수신
```python
def receive_etttp_message(socket):
    try:
        message = socket.recv(1024).decode('utf-8')
        return message
    except Exception as e:
        print(f"수신 에러: {e}")
        return None
```

## 🧪 프로토콜 테스팅

### 단위 테스트
```python
def test_message_parsing():
    message = "SEND ETTTP/1.0\r\nHost: 127.0.0.1\r\nNew-Move: (1, 2)\r\n\r\n"
    assert parse_etttp_message(message) is not None

def test_coordinate_validation():
    assert validate_coordinates("(1, 2)") == True
    assert validate_coordinates("(3, 1)") == False
    assert validate_coordinates("invalid") == False
```

### 통합 테스트
```python
def test_full_game_protocol():
    # 완전한 메시지 교환 순서 테스트
    # 적절한 상태 전환 검증
    # 결과 일관성 확인
    pass
```

### 수동 테스트 시나리오
1. **정상 게임 플로우**: 적절한 움직임으로 완전한 게임
2. **유효하지 않은 메시지**: 잘못된 ETTTP 메시지 전송
3. **연결 끊김**: 게임 중간에 연결 해제
4. **빠른 움직임**: 빠른 연속 움직임 시도
5. **엣지 케이스**: 모서리 및 중앙 움직임, 즉시 승리

## 📊 성능 고려사항

### 메시지 크기
- 일반적인 메시지: ~50-100 바이트
- 권장 최대값: 1024 바이트
- 최소 오버헤드 설계

### 지연시간 요구사항
- 움직임 확인: < 100ms
- 전체 왕복 시간: < 200ms
- 실시간 게임플레이에 적합

### 신뢰성
- TCP가 전달 및 순서 보장
- 움직임 검증을 위한 애플리케이션 수준 ACK
- 에러 감지 및 연결 복구

## 🔒 보안 고려사항

### 입력 검증
- 모든 수신 메시지 검증 필수
- 좌표 경계 확인 필수
- 프로토콜 형식 엄격 적용

### 서비스 거부 공격
- 연결 타임아웃으로 행(hanging) 방지
- 버퍼 오버플로우 방지를 위한 메시지 크기 제한
- 움직임 빈도 제한

### 데이터 무결성
- 체크섬 검증 (향후 개선사항)
- 메시지 순서 검증
- 상태 일관성 확인

## 🌐 로컬라이제이션 (한국어)

### 에러 메시지
```python
ERROR_MESSAGES = {
    'INVALID_FORMAT': '잘못된 ETTTP 메시지 형식입니다.',
    'INVALID_COORDINATES': '좌표가 유효 범위를 벗어났습니다.',
    'NOT_YOUR_TURN': '현재 당신의 턴이 아닙니다.',
    'CELL_OCCUPIED': '이미 점유된 셀입니다.',
    'CONNECTION_LOST': '연결이 끊어졌습니다.'
}
```

### 디버그 출력
```python
def debug_log(message, level='INFO'):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {level}: {message}")

# 사용 예시
debug_log("ETTTP 메시지 수신: SEND ETTTP/1.0...")
debug_log("좌표 (1,2)에 움직임 처리 중...")
debug_log("상대방에게 ACK 전송 완료")
```

### 사용자 인터페이스 메시지
```python
UI_MESSAGES = {
    'WAITING_CONNECTION': '연결을 기다리는 중...',
    'GAME_STARTED': '게임이 시작되었습니다!',
    'YOUR_TURN': '당신의 차례입니다',
    'OPPONENT_TURN': '상대방의 차례입니다',
    'YOU_WIN': '당신이 승리했습니다!',
    'YOU_LOSE': '당신이 패배했습니다!',
    'DRAW': '무승부입니다!'
}
```

## 📚 구현 예시

### 완전한 메시지 교환 예시
```python
# 서버측 초기 설정
def send_first_move(client_socket, first_player):
    headers = {
        'Host': '127.0.0.1',
        'First-Move': 'YOU' if first_player == 1 else 'ME'
    }
    return send_etttp_message(client_socket, 'SEND', headers)

# 클라이언트측 응답
def send_ack_first_move(server_socket, first_move_value):
    headers = {
        'Host': '127.0.0.1',
        'First-Move': first_move_value
    }
    return send_etttp_message(server_socket, 'ACK', headers)

# 게임 움직임 전송
def send_game_move(socket, row, col, peer_ip):
    headers = {
        'Host': peer_ip,
        'New-Move': f'({row}, {col})'
    }
    return send_etttp_message(socket, 'SEND', headers)

# 결과 전송
def send_game_result(socket, result, peer_ip):
    headers = {
        'Host': peer_ip,
        'Winner': result  # 'ME', 'YOU', 또는 'DRAW'
    }
    return send_etttp_message(socket, 'RESULT', headers)
```

---

**프로토콜 버전**: 1.0  
**최종 업데이트**: 2025년 5월 26일  
**상태**: 구현 초안

## 📖 추가 참고자료

### 관련 RFC 및 표준
- **RFC 793**: TCP 프로토콜 명세
- **RFC 2616**: HTTP/1.1 (헤더 형식 참조)
- **RFC 5234**: ABNF 구문 명세

### 구현 팁
- **메시지 파싱**: 정규표현식보다 문자열 분할 사용 권장
- **에러 처리**: 가능한 한 구체적인 에러 메시지 제공
- **테스팅**: 실제 네트워크 환경에서 테스트 필수
- **디버깅**: 와이어샤크 등 네트워크 분석 도구 활용 고려