# agent-browser 정리 (Vercel Labs)

> 원본: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) (Apache-2.0) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+8k stars)

**AI 에이전트가 셸에서 명령 하나씩으로 브라우저를 조작하는 Rust CLI.** 페이지를 접근성 트리 텍스트로 읽고(`@e1` 같은 ref), ref로 요소를 조작한다. 셸 명령이라 특정 하네스에 묶이지 않고, MCP 서버 모드(`agent-browser mcp`)도 있다. macOS / Linux / Windows.

## 설치
```bash
npm install -g agent-browser
agent-browser install           # Chrome for Testing 다운로드 (처음 한 번)
# 또는: brew install agent-browser / 설치 없이: npx agent-browser open example.com
```

## 기본 루프
```bash
agent-browser open example.com
agent-browser snapshot -i       # 인터랙티브 요소만, 각각 ref 포함
agent-browser click @e1         # snapshot에서 받은 ref로 조작
agent-browser get url           # 결과 확인
agent-browser close
```
- **ref는 snapshot 시점 기준**: 페이지 이동이나 DOM 변경 후에는 snapshot을 다시 찍기
- 대상이 숨김, 비활성, 가려짐이면 click이 성공으로 보고하지 않고 실패함
- semantic locator도 가능: `agent-browser find role button click --name "Submit"`

## 에이전트에 붙이기
```bash
agent-browser skills get core                 # 핵심 루프, ref, 대기, 공통 워크플로
agent-browser skills get core --full          # 전체 명령 레퍼런스 포함
agent-browser skills list                     # electron, slack, dogfood 등 전문 스킬
npx skills add vercel-labs/agent-browser
```
`AGENTS.md` / `CLAUDE.md`에 넣을 문구:
```markdown
Use `agent-browser` for browser automation. Before the first use, run
`agent-browser skills get core` and follow it.
```

## 명령 그룹
| 그룹 | 명령 |
|---|---|
| 탐색/읽기 | `open`, `back`, `forward`, `reload`, `read`, `snapshot`, `get`, `is` |
| 상호작용 | `click`, `fill`, `type`, `press`, `hover`, `select`, `check`, `scroll`, `drag`, `upload`, `find` |
| 캡처 | `screenshot`, `pdf`, `record`, `download`, `diff` |
| 상태/네트워크 | `cookies`, `storage`, `network`, `eval` |
| 디버그/성능 | `console`, `errors`, `trace`, `profiler`, `vitals`, `a11y` |
| 세션 | `session`, `state`, `auth`, `profiles` |

- `--session`마다 브라우저 분리 (병렬 작업, 계정 분리)
- `--cdp` / `--auto-connect`로 이미 로그인된 실제 Chrome에 연결
- 클라우드 브라우저: Browserbase, Browserless, Browser Use 등 (별도 계정)

## 응용 아이디어
- "snapshot → ref로 행동 → 다시 snapshot으로 확인" 루프를 에이전트 규칙으로 쓰면 컨텍스트가 작아진다 → [08-agent-instructions](../08-agent-instructions)
- 스킬 본문을 CLI에서 가져오게(`skills get core`) 해서 CLI 버전과 지침을 항상 일치시키기
- `diff`, `record`, `screenshot`으로 QA 증빙 남기기 → [05-code-inspection](../05-code-inspection)

## 주의
- 실제 Chrome에 붙이면 로그인 세션, 쿠키, 저장소에 접근 가능. `cookies`, `storage`, `eval` 권한 주의
