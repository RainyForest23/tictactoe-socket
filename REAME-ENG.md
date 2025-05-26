# 🎮 Tic-Tac-Toe Socket Programming

**정보통신공학 Term Project**  
**Due**: June 1, 2025 11:59 PM  
**Team**: 2 Members

## 📋 Project Overview

An online multiplayer Tic-Tac-Toe game implemented using TCP socket programming with a custom application protocol called **ETTTP (Ewha Tic-Tac-Toe Protocol)**.

### 🎯 Key Features
- **Real-time multiplayer gameplay** over TCP connection
- **Custom ETTTP protocol** for message exchange
- **Peer-to-peer functionality** with client-server architecture
- **Interactive GUI** built with Python Tkinter
- **Game result verification** system
- **Debug mode** for protocol testing

## 🏗️ Architecture

```
Client ←→ TCP Socket (Port 12000) ←→ Server
    ↓                                    ↓
  GUI (Tkinter)                    GUI (Tkinter)
    ↓                                    ↓
ETTTP Protocol ←→ Game Logic ←→ ETTTP Protocol
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- Socket support

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/tictactoe-socket.git
cd tictactoe-socket
```

2. **Test your environment**
```bash
python tests/test_environment.py
```

### Usage

1. **Start the Server** (Terminal 1)
```bash
python src/ETTTP_Server_skeleton.py
```

2. **Start the Client** (Terminal 2)  
```bash
python src/ETTTP_Client_skeleton.py
```

3. **Play the Game**
   - Server randomly decides who goes first
   - Players take turns clicking on the 3x3 grid
   - Real-time synchronization between both players
   - Game ends when someone wins or draws

## 🎮 Game Rules

- **Board**: 3x3 grid (positions 0-8)
- **Marks**: X (first player) and O (second player)
- **Turns**: Only the active player can make moves
- **Win Condition**: Three marks in a row (horizontal, vertical, or diagonal)
- **Status**: Green "Ready" or Red "Hold" indicator

## 🔌 ETTTP Protocol

### Message Types

1. **Initial Setup** (Server → Client)
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
First-Move: YOU \r\n
\r\n
```

2. **Game Move** (Bidirectional)
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
New-Move: (1, 2) \r\n
\r\n
```

3. **Acknowledgment** (Bidirectional)
```
ACK ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
New-Move: (1, 2) \r\n
\r\n
```

4. **Result Verification** (Bidirectional)
```
RESULT ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
Winner: ME \r\n
\r\n
```

## 📁 Project Structure

```
tictactoe-socket/
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
├── CONTRIBUTING.md                # Collaboration guidelines
├── src/
│   ├── ETTTP_Server_skeleton.py   # Server implementation
│   ├── ETTTP_Client_skeleton.py   # Client implementation
│   └── ETTTP_TicTacToe_skeleton.py # Game logic and GUI
├── tests/
│   ├── test_environment.py        # Environment validation
│   ├── gui_test.py                # GUI functionality test
│   └── socket_test.py             # Socket connection test
├── docs/
│   ├── ETTTP_Protocol.md          # Protocol specification
│   ├── Implementation_Guide.md    # Development guide
│   └── screenshots/               # Game screenshots
└── report/
    ├── final_report.md            # Project report
    └── assets/                    # Report images
```

## 🛠️ Development

### Implementation Status

- [x] Project setup and protocol design
- [ ] Server-side ETTTP implementation
- [ ] Client-side ETTTP implementation  
- [ ] Game logic and GUI integration
- [ ] Result verification system
- [ ] Testing and debugging
- [ ] Documentation and report

### Key Functions to Implement

| Function | File | Description | Priority |
|----------|------|-------------|----------|
| `check_msg()` | TicTacToe | ETTTP message validation | High |
| `get_move()` | TicTacToe | Receive and process moves | High |
| `send_move()` | TicTacToe | Send moves to peer | High |
| `check_result()` | TicTacToe | Game result verification | Medium |
| `send_debug()` | TicTacToe | Debug mode messaging | Low |

## 🧪 Testing

### Environment Test
```bash
python tests/test_environment.py
```

### GUI Test  
```bash
python tests/gui_test.py
```

### Socket Test
```bash
python tests/socket_test.py
```

### Integration Test (Loopback)
1. Run server: `python src/ETTTP_Server_skeleton.py`
2. Run client: `python src/ETTTP_Client_skeleton.py`  
3. Test various game scenarios

## 🐛 Debug Mode

The game includes a debug mode where you can manually input ETTTP messages:

1. Click in the text box at the bottom
2. Type or paste an ETTTP message
3. Click "Send" to transmit
4. Monitor the response

Example debug input:
```
SEND ETTTP/1.0 \r\n
Host: 127.0.0.1 \r\n
New-Move: (1, 1) \r\n
\r\n
```

## 📝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Branch Strategy
- `main`: Production-ready code
- `feature/server-impl`: Server implementation
- `feature/client-impl`: Client implementation  
- `feature/protocol`: Protocol-related functions

### Commit Convention
```
feat: add new feature
fix: bug fix
docs: documentation changes
test: test code changes
refactor: code refactoring
```

## 📊 Grading Criteria

- **Accuracy (60%)**: Correctness of implementation
- **Code Analysis (30%)**: Technical report quality  
- **Code Comments (10%)**: Code documentation quality

## 🔧 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Kill process using port 12000
lsof -ti:12000 | xargs kill -9
```

**tkinter Import Error**
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On macOS
brew install python-tk
```

**Socket Connection Refused**
- Ensure server is running before starting client
- Check firewall settings
- Verify port 12000 is available

## 👥 Team Members

- **Person A**: Server implementation and protocol design
- **Person B**: Client implementation and testing

## 📄 License

This project is for educational purposes as part of Information Communications course.

## 📞 Contact

For questions regarding this project, please contact:
- **Person A**: exampleA@ewhain.net
- **Person B**: exampleB@ewhain.net

---

**Last Updated**: May 26, 2025  
**Version**: 1.0.0