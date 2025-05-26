# 🤝 협업 가이드라인

이 문서는 틱택토 소켓 프로그래밍 프로젝트의 협업 가이드라인을 설명합니다.

## 👥 팀 구조

- **팀 크기**: 2명
- **담당자 A**: 서버 구현 리드
- **담당자 B**: 클라이언트 구현 리드
- **공동 책임**: 프로토콜 설계, 테스팅, 문서화

## 🌟 개발 워크플로우

### 1. 일일 워크플로우

#### 오전 (오전 9시)
- [ ] `main` 브랜치에서 최신 변경사항 pull
- [ ] 팀원의 밤사이 커밋 검토
- [ ] 일일 목표 및 작업 계획 수립

#### 저녁 (오후 8시) - 일일 스탠드업 (10분)
- **오늘 무엇을 완료했나요?**
- **내일 무엇을 작업할 예정인가요?**
- **막히는 부분이나 도움이 필요한 것이 있나요?**
- **코드 리뷰 요청사항이 있나요?**

### 2. 브랜치 전략

```
main
├── feature/server-impl        # 담당자 A의 메인 브랜치
├── feature/client-impl        # 담당자 B의 메인 브랜치
├── feature/protocol           # 공유 프로토콜 함수
├── hotfix/urgent-bugs         # 긴급 버그 수정
└── docs/report               # 문서화 및 보고서
```

#### 브랜치 명명 규칙
```
feature/기능설명           # 새로운 기능
fix/버그설명              # 버그 수정  
docs/문서업데이트         # 문서화
test/테스트설명           # 테스트 코드
refactor/코드정리         # 코드 리팩토링
```

### 3. 커밋 가이드라인

#### 커밋 메시지 형식
```
<타입>(<범위>): <제목>

<본문>

<푸터>
```

#### 타입들
- **feat**: 새로운 기능
- **fix**: 버그 수정
- **docs**: 문서 변경
- **style**: 코드 스타일 변경 (포맷팅 등)
- **refactor**: 코드 리팩토링
- **test**: 테스트 추가 또는 업데이트
- **chore**: 유지보수 작업

#### 예시들
```
feat(server): ETTTP 메시지 파싱 구현

- 프로토콜 검증을 위한 check_msg() 함수 추가
- 잘못된 메시지 에러 처리
- 메시지 파싱을 위한 단위 테스트 추가

Closes #12

fix(client): 소켓 연결 타임아웃 해결

- 연결 타임아웃을 10초로 증가
- 실패한 연결에 대한 재시도 메커니즘 추가
- 에러 처리 및 사용자 피드백 개선

test(protocol): ETTTP 메시지 검증 테스트 추가

- 유효한 메시지 형식 테스트
- 유효하지 않은 메시지 처리 테스트
- 잘못된 헤더에 대한 엣지 케이스 추가
```

## 🔄 코드 리뷰 과정

### Pull Request 요구사항

#### PR 생성 전
- [ ] 코드가 에러 없이 컴파일됨
- [ ] 모든 기존 테스트 통과
- [ ] 새로운 기능에 대한 새 테스트 추가
- [ ] 프로젝트 스타일 가이드라인 준수
- [ ] 필요시 문서 업데이트
- [ ] 셀프 리뷰 완료

#### PR 템플릿
```markdown
## 📝 설명
변경사항에 대한 간략한 설명

## 🔧 변경 유형
- [ ] 버그 수정
- [ ] 새로운 기능
- [ ] 문서 업데이트
- [ ] 리팩토링

## 🧪 테스팅
- [ ] 단위 테스트 추가/업데이트
- [ ] 통합 테스트 통과
- [ ] 수동 테스트 완료

## 📋 체크리스트
- [ ] 코드가 스타일 가이드라인을 따름
- [ ] 셀프 리뷰 완료
- [ ] 문서 업데이트됨
- [ ] 병합 충돌 없음

## 🔗 관련 이슈
Closes #이슈번호
```

#### 리뷰 가이드라인
- **응답 시간**: 24시간 이내
- **승인 필요**: 최소 1명의 팀원 승인
- **리뷰 초점**:
  - 코드 정확성 및 로직
  - ETTTP 프로토콜 준수
  - 에러 처리 완성도
  - 코드 가독성 및 주석
  - 테스트 커버리지

## 📝 코딩 표준

### Python 스타일 가이드

#### 코드 포맷팅
```python
# 함수 명명: snake_case
def send_etttp_message(socket, message):
    pass

# 클래스 명명: PascalCase  
class TTTGameLogic:
    pass

# 상수: UPPER_CASE
BUFFER_SIZE = 1024
DEFAULT_PORT = 12000

# 변수 명명: 설명적이고 명확하게
client_socket = socket(AF_INET, SOCK_STREAM)
message_buffer = ""
is_valid_move = True
```

#### 문서화 표준
```python
def check_msg(msg, recv_ip):
    """
    ETTTP 프로토콜 메시지 형식을 검증합니다.
    
    Args:
        msg (str): 소켓에서 받은 원본 메시지
        recv_ip (str): 예상되는 발신자 IP 주소
        
    Returns:
        bool: 메시지가 유효하면 True, 그렇지 않으면 False
        
    Raises:
        ValueError: 메시지 형식이 유효하지 않은 경우
        
    Example:
        >>> check_msg("SEND ETTTP/1.0\\r\\n...", "127.0.0.1")
        True
    """
    pass
```

#### 에러 처리
```python
# 좋은 예: 구체적인 예외 처리
try:
    socket.send(message.encode())
except ConnectionError as e:
    print(f"연결 실패: {e}")
    return False
except Exception as e:
    print(f"예상치 못한 오류: {e}")
    return False

# 나쁜 예: 일반적인 except
try:
    socket.send(message.encode())
except:
    return False
```

### GUI 표준

#### Tkinter 모범 사례
```python
# UI 요소의 명확한 변수 명명
self.status_label = tk.Label(...)
self.game_board_frame = tk.Frame(...)
self.send_button = tk.Button(...)

# 일관된 스타일링
BUTTON_STYLE = {
    'font': ('Arial', 12),
    'bg': '#4CAF50',
    'fg': 'white'
}

# 이벤트 핸들러 명명
def on_cell_click(self, event, cell_index):
    pass

def on_send_button_click(self):
    pass
```

## 🧪 테스팅 가이드라인

### 테스트 카테고리

#### 1. 단위 테스트
```python
# test_protocol.py
def test_valid_etttp_message():
    message = "SEND ETTTP/1.0\r\nHost: 127.0.0.1\r\nNew-Move: (1, 2)\r\n\r\n"
    assert check_msg(message, "127.0.0.1") == True

def test_invalid_etttp_format():
    message = "INVALID FORMAT"
    assert check_msg(message, "127.0.0.1") == False
```

#### 2. 통합 테스트
```python
# test_game_flow.py
def test_complete_game_flow():
    # 연결부터 결과까지 전체 게임 테스트
    pass

def test_connection_handling():
    # 소켓 연결/해제 테스트
    pass
```

#### 3. 수동 테스트 시나리오
- [ ] 정상적인 게임 완료 (승리/패배/무승부)
- [ ] 연결 중단 처리
- [ ] 유효하지 않은 움직임 시도
- [ ] 메시지 형식 위반
- [ ] GUI 반응성

### 테스팅 체크리스트

#### 각 커밋 전
- [ ] 모든 단위 테스트 통과
- [ ] 수동 스모크 테스트 완료
- [ ] 콘솔 에러 없음
- [ ] GUI 정상 작동

#### PR 제출 전  
- [ ] 통합 테스트 통과
- [ ] 크로스 플랫폼 테스트 (해당시)
- [ ] 성능 테스트
- [ ] 엣지 케이스 테스트

## 🚀 릴리스 과정

### 버전 관리
- **v0.1.0**: 기본 프로토콜 구현
- **v0.2.0**: 게임 로직 완성
- **v0.3.0**: GUI 통합
- **v1.0.0**: 최종 제출 버전

### 릴리스 체크리스트
- [ ] 모든 기능 구현 완료
- [ ] 모든 테스트 통과
- [ ] 문서화 완료
- [ ] 코드 리뷰 완료
- [ ] 성능 수용 가능
- [ ] 제출 준비 완료

## 🔧 개발 도구

### 권장 IDE 설정
```
VS Code 확장프로그램:
- Python
- GitLens
- Python Docstring Generator
- Bracket Pair Colorizer

PyCharm 설정:
- PEP 8 검사 활성화
- Git 통합 설정
- 코드 템플릿 설정
```

### 필수 도구
- **Python 3.7+**: 핵심 개발
- **Git**: 버전 관리
- **터미널**: 서버/클라이언트 실행
- **텍스트 에디터**: 코드 편집

## 📋 소통 프로토콜

### 회의 일정
- **일일 체크인**: 오후 8시 (10분)
- **주중 리뷰**: 수요일 오후 7시 (30분)
- **주말 계획**: 일요일 오후 6시 (20분)

### 소통 채널
- **GitHub Issues**: 버그 리포트 및 기능 요청
- **GitHub PR Comments**: 코드 리뷰 토론
- **카카오톡/디스코드**: 빠른 질문 및 조율
- **화상 통화**: 복잡한 문제 해결

### 응급 절차
- **긴급 버그**: 전화/문자로 즉시 알림
- **작업 차단**: GitHub 이슈 생성 및 팀 알림
- **마감일 누락**: 24시간 사전 통보 필요

## 🎯 완료 정의

### 기능 완료
- [ ] 코드 구현 및 테스트됨
- [ ] 단위 테스트 작성 및 통과
- [ ] 통합 테스트 완료
- [ ] 코드 리뷰 및 승인
- [ ] 문서 업데이트
- [ ] 알려진 버그 없음

### 스프린트 완료
- [ ] 계획된 모든 기능 완료
- [ ] 모든 테스트 통과
- [ ] 코드 커버리지 요구사항 충족
- [ ] 성능 벤치마크 달성
- [ ] 다음 스프린트 준비 완료

## 📞 도움 받기

### 언제 도움을 요청할까
- 구현에서 2시간 이상 막힌 경우
- 요구사항이나 명세가 불분명한 경우
- 진행을 막는 기술적 장애물
- 설계/아키텍처 결정이 필요한 경우

### 도움 요청 방법
1. **문제 문서화**: 예시와 함께 명확한 설명
2. **시도한 것 보여주기**: 이전 시도 및 조사 내용
3. **구체적으로**: 정확한 에러 메시지나 동작
4. **컨텍스트 제공**: 관련 코드 및 환경 세부사항

### 에스컬레이션 경로
1. **팀원**: 모든 이슈에 대한 첫 번째 연락처
2. **온라인 리소스**: Stack Overflow, 문서
3. **교수님**: 과목 관련 질문만

## 🇰🇷 한국어 특화 가이드

### 커밋 메시지 (한국어 버전)
```
기능: 서버 ETTTP 메시지 파싱 구현
수정: 클라이언트 소켓 연결 타임아웃 해결
문서: 프로토콜 명세 업데이트
테스트: GUI 기능 테스트 추가
리팩터: 코드 정리 및 최적화
```

### 주석 작성 가이드
```python
# 한국어 주석 - 복잡한 로직 설명용
def complex_function():
    # 복잡한 비즈니스 로직에 대한 한국어 설명
    # 팀원이 이해하기 쉽게 작성
    pass

# 영어 docstring - 공식 문서화용  
def public_function():
    """
    Official function documentation in English
    for consistency with Python standards.
    """
    pass
```

### 변수 명명 (한국어 컨텍스트)
```python
# 좋은 예: 영어로 명명하되 의미가 명확하게
server_socket = socket(AF_INET, SOCK_STREAM)
client_connection = None
game_board_state = [0] * 9
current_player_turn = True

# 피할 것: 한국어 변수명 (인코딩 문제 가능성)
# 서버소켓 = socket(AF_INET, SOCK_STREAM)  # 권장하지 않음
```

---

**기억하세요**: 좋은 소통과 협업이 좋은 코드만큼 중요합니다! 🎉

## 📚 추가 리소스

### 학습 자료
- **Python 소켓 프로그래밍**: https://docs.python.org/3/howto/sockets.html
- **Tkinter 튜토리얼**: https://docs.python.org/3/library/tkinter.html
- **Git 가이드**: https://git-scm.com/book/ko/v2

### 도움되는 도구
- **온라인 정규식 테스터**: https://regex101.com/
- **JSON 포맷터**: https://jsonformatter.org/
- **네트워크 디버거**: Wireshark (고급 사용자용)

### 이화여대 리소스
- **컴퓨터공학과 홈페이지**: 과목 관련 공지사항
- **사이버캠퍼스**: 과제 제출 및 자료 다운로드
- **도서관 전자자료**: 기술 서적 및 논문 검색