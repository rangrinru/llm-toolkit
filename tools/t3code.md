# T3 Code 정리

> 원본: [pingdotgg/t3code](https://github.com/pingdotgg/t3code) (MIT) | 홈페이지: https://t3.codes | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+35k stars)

**"코딩 에이전트를 위한 오픈소스 컨트롤 플레인."** 내 컴퓨터에서 Claude Code, Codex 등을 실행하고, 하나의 인터페이스(데스크톱, 웹, iOS/Android)에서 제어한다. 책상에서 시작한 작업을 폰에서 이어서 승인할 수 있다.
- 지원: Claude Code, Codex, Cursor, OpenCode, Grok Build, Antigravity, Kiro, Pi 등 + 모든 ACP 에이전트

## 핵심 기능
- **구독 그대로 사용**: 토큰을 재판매하지 않고, 이미 로그인된 에이전트를 구동
- **여러 에이전트를 한 곳에서**: 작업(thread) 도중 모델 변경, Claude가 Codex에 작업을 넘기기도 가능
- **데스크톱, 웹, 폰이 같은 thread를 봄**. 로컬 네트워크, Tailscale, T3 Connect로 원격 접속
- **Git 내장**: thread마다 worktree, diff 검토 후 버튼 하나로 commit, push, PR
- **권한 모드 4종**: Supervised, Auto-accept edits, Auto, Full access
- **MCP 서버**(`https://<environment-address>/mcp`)로 외부 에이전트가 thread를 조회하고 시작 가능

## 설치
```bash
brew install --cask t3-code                 # macOS
winget install T3Tools.T3Code               # Windows (또는 scoop install extras/t3code)
curl -fsSL https://t3.codes/install.sh | sh # CLI (t3 실행 시 서버 + 웹앱)
npx t3@latest                               # 설치 없이 1회 실행
```
- 먼저 에이전트 로그인 필요: `claude auth login`, `codex login`

## 워크플로 위치
에이전트 CLI 위에 얹는 GUI/제어 계층. thread 생성 → 에이전트 실행 → worktree에서 diff 검토 → PR. 자리를 비운 사이 승인 요청이 오면 폰에서 처리.
→ [09-workflows/development](../09-workflows/development)

## 응용 아이디어
- 같은 작업을 Claude와 Codex thread로 나눠 돌리고 비교하거나 넘기기
- 집/회사 컴퓨터에서 에이전트를 돌려두고 폰으로 승인만
- 터미널 에이전트가 T3의 MCP 서버로 thread를 만들어 오케스트레이션

## 주의
- **초기 권한 기본값이 Full access** → Settings → Threads에서 조정 권장
- 비용은 연결한 에이전트 구독 기준
