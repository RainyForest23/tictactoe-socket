# 🎮 Tic-Tac-Toe Socket Programming

**정보통신공학 Term Project**  
**마감일**: 2025년 6월 1일 오후 11시 59분  
**팀 구성**: 2명

## 📋 프로젝트 개요

TCP 소켓 프로그래밍을 사용하여 구현된 온라인 멀티플레이어 틱택토 게임입니다. **ETTTP (Ewha Tic-Tac-Toe Protocol)**라는 커스텀 애플리케이션 프로토콜을 사용합니다.

### 🎯 주요 기능
- **실시간 멀티플레이어 게임플레이** (TCP 연결 기반)
- **커스텀 ETTTP 프로토콜**을 통한 메시지 교환
- **클라이언트-서버 구조**의 피어투피어 기능
- **Python Tkinter**로 구축된 인터랙티브 GUI
- **게임 결과 검증** 시스템
- **프로토콜 테스팅**을 위한 디버그 모드

## 🏗️ 시스템 구조

```
클라이언트 ←→ TCP 소켓 (포트 12000) ←→ 서버
    ↓                                    ↓
  GUI (Tkinter)                    GUI (Tkinter)
    ↓                                    ↓
ETTTP 프로토콜 ←→ 게임 로직 ←→ ETTTP 프로토콜
```

## 🚀 빠른 시작

### 사전 준비 사항
- Python 3.7 이상
- tkinter (보통 Python과 함께 설치됨)
- 소켓 지원

### 설치 방법

1. **저장소 클론**
```bash
git clone https://github.com/your-username/tictactoe-socket.git
cd tictactoe-socket
```

2. **환경 테스트**
```bash
python tests/test_environment.py
```

### 사용 방법

1. **서버 시작** (터미널 1)
```bash
python src/ETTTP_Server_skeleton.py
```

2. **클라이언트 시작** (터미널 2)  
```bash
python src/ETTTP_Client_skeleton.py
```

3. **게임 플레이**
   - 서버가 무작위로 선턴을 결정
   - 플레이어들이 번갈아가며 3x3 그리드 클릭
   - 양쪽 플레이어 간 실시간 동기화
   - 누군가 이기거나 무승부가 되면 게임 종료

## 🎮 게임 규칙

- **보드**: 3x3 그리드 (위치 0-8)
- **마크**: X (첫 번째 플레이어), O (두 번째 플레이어)
- **턴**: 활성 플레이어만 움직임 가능
- **승리 조건**: 가로, 세로, 대각선으로 세 개 연속
- **상태**: 초록색 "Ready" 또는 빨간색 "Hold" 표시

## 🔌 ETTTP 프로토콜

### 메시지 유형

1. **초기 설정** (서버 → 클라이언트)
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
First-Move: YOU \r\n
\r\n
```

2. **게임 움직임** (양방향)
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
New-Move: (1, 2) \r\n
\r\n
```

3. **확인 응답** (양방향)
```
ACK ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
New-Move: (1, 2) \r\n
\r\n
```

4. **결과 검증** (양방향)
```
RESULT ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
Winner: ME \r\n
\r\n
```

## 📁 프로젝트 구조

```
tictactoe-socket/
├── README.md                      # 이 파일 (영어)
├── README_KR.md                   # 이 파일 (한국어)
├── .gitignore                     # Git 무시 규칙
├── CONTRIBUTING.md                # 협업 가이드라인 (영어)
├── CONTRIBUTING_KR.md             # 협업 가이드라인 (한국어)
├── src/
│   ├── ETTTP_Server_skeleton.py   # 서버 구현
│   ├── ETTTP_Client_skeleton.py   # 클라이언트 구현
│   └── ETTTP_TicTacToe_skeleton.py # 게임 로직 및 GUI
├── tests/
│   ├── test_environment.py        # 환경 검증
│   ├── gui_test.py                # GUI 기능 테스트
│   └── socket_test.py             # 소켓 연결 테스트
├── docs/
│   ├── ETTTP_Protocol.md          # 프로토콜 명세 (영어)
│   ├── ETTTP_Protocol_KR.md       # 프로토콜 명세 (한국어)
│   ├── Implementation_Guide.md    # 개발 가이드
│   └── screenshots/               # 게임 스크린샷
└── report/
    ├── final_report.md            # 프로젝트 보고서
    └── assets/                    # 보고서 이미지
```

## 🛠️ 개발 현황

### 구현 상태

- [x] 프로젝트 설정 및 프로토콜 설계
- [ ] 서버측 ETTTP 구현
- [ ] 클라이언트측 ETTTP 구현  
- [ ] 게임 로직 및 GUI 통합
- [ ] 결과 검증 시스템
- [ ] 테스팅 및 디버깅
- [ ] 문서화 및 보고서

### 구현해야 할 주요 함수들

| 함수명 | 파일 | 설명 | 우선순위 |
|----------|------|-------------|----------|
| `check_msg()` | TicTacToe | ETTTP 메시지 검증 | 높음 |
| `get_move()` | TicTacToe | 움직임 수신 및 처리 | 높음 |
| `send_move()` | TicTacToe | 움직임을 상대방에게 전송 | 높음 |
| `check_result()` | TicTacToe | 게임 결과 검증 | 중간 |
| `send_debug()` | TicTacToe | 디버그 모드 메시징 | 낮음 |

## 🧪 테스팅

### 환경 테스트
```bash
python tests/test_environment.py
```

### GUI 테스트  
```bash
python tests/gui_test.py
```

### 소켓 테스트
```bash
python tests/socket_test.py
```

### 통합 테스트 (루프백)
1. 서버 실행: `python src/ETTTP_Server_skeleton.py`
2. 클라이언트 실행: `python src/ETTTP_Client_skeleton.py`  
3. 다양한 게임 시나리오 테스트

## 🐛 디버그 모드

게임에는 ETTTP 메시지를 수동으로 입력할 수 있는 디버그 모드가 포함되어 있습니다:

1. 하단의 텍스트 박스 클릭
2. ETTTP 메시지 타이핑 또는 붙여넣기
3. "Send" 버튼 클릭하여 전송
4. 응답 모니터링

디버그 입력 예시:
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
New-Move: (1, 1) \r\n
\r\n
```

## 📝 기여하기

Pull Request 제출 과정에 대한 자세한 내용은 [CONTRIBUTING_KR.md](CONTRIBUTING_KR.md)를 참조하세요.

### 브랜치 전략
- `main`: 완성된 코드
- `feature/server-impl`: 서버 구현
- `feature/client-impl`: 클라이언트 구현  
- `feature/protocol`: 프로토콜 관련 함수

### 커밋 규칙
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
test: 테스트 코드 수정
refactor: 코드 리팩토링
```

## 📊 채점 기준

- **정확성 (60%)**: 구현의 정확성
- **코드 분석 (30%)**: 기술 보고서 품질  
- **코드 주석 (10%)**: 코드 문서화 품질

## 🔧 문제 해결

### 일반적인 문제들

**포트가 이미 사용 중인 경우**
```bash
# 포트 12000을 사용하는 프로세스 종료
lsof -ti:12000 | xargs kill -9
```

**tkinter 임포트 에러**
```bash
# Ubuntu/Debian에서
sudo apt-get install python3-tk

# macOS에서
brew install python-tk
```

**소켓 연결 거부됨**
- 클라이언트 시작 전에 서버가 실행 중인지 확인
- 방화벽 설정 확인
- 포트 12000이 사용 가능한지 확인
**
## 👥 팀 구성원

- **담당자 A**: 서버 구현 및 프로토콜 설계
- **담당자 B**: 클라이언트 구현 및 테스팅

## 📞 연락처

이 프로젝트에 관한 질문은 다음으로 연락주세요:
- **담당자 A**: exampleA@ewhain.net
- **담당자 B**: exampleB@ewhain.net**

---

**최종 업데이트**: 2025년 5월 26일  
**버전**: 1.0.0

## 🇰🇷 한국어 지원

이 프로젝트는 한국어 문서를 제공합니다:
- [README_KR.md](README_KR.md) - 프로젝트 개요 (이 문서)
- [CONTRIBUTING_KR.md](CONTRIBUTING_KR.md) - 협업 가이드라인
- [ETTTP_Protocol_KR.md](docs/ETTTP_Protocol_KR.md) - 프로토콜 명세

English documentation is also available:
- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Collaboration guidelines  
- [ETTTP_Protocol.md](docs/ETTTP_Protocol.md) - Protocol specification