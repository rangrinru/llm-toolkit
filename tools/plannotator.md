# Plannotator 정리

> 원본: [backnotprop/plannotator](https://github.com/backnotprop/plannotator) (Apache-2.0 / MIT) | 홈페이지: plannotator.ai | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+3.5k stars)

**AI 코딩 에이전트용 로컬 브라우저 리뷰 화면.** 에이전트의 계획(plan), 스펙, markdown, HTML, diff, PR에 주석을 달고 구조화된 피드백을 에이전트에 돌려보낸다.
- 지원: Claude Code, Codex, Copilot CLI, Gemini CLI, OpenCode, Kiro, Amp, Pi, T3 Code 등

## 핵심 기능
- **Plan review**: 에이전트가 계획을 내면 브라우저가 자동으로 열림 → 승인하면 진행, 거부하면 주석이 피드백으로 전달 → 수정된 계획은 diff로 표시
- **Annotate**: markdown 파일/폴더, URL, HTML, 에이전트의 마지막 메시지, 실행 중인 localhost 사이트에 주석
- **Code review**: 로컬 변경, GitHub PR, GitLab MR 검토 + 코드 제안
- **Guided review** (`Cmd/Ctrl+Shift+G`): 에이전트가 diff를 중요도순 챕터로 정렬
- **Inbox**: 여러 에이전트의 질문, 결정, 파일을 한 창에
- **공유**: 링크 공유, 팀원 피드백 가져오기 (큰 공유는 암호화, 7일 후 만료)
- 연동: VS Code, Obsidian(승인된 plan 자동 저장), Notion

## 설치
```bash
curl -fsSL https://plannotator.ai/install.sh | bash      # macOS / Linux / WSL
irm https://plannotator.ai/install.ps1 | iex             # Windows PowerShell
```
```text
# Claude Code (설치 후 재시작)
/plugin marketplace add backnotprop/plannotator
/plugin install plannotator@plannotator
```
- Codex, Gemini CLI, Kiro는 설치 프로그램이 자동 설정. OpenCode는 `opencode.json`에 `"plugin": ["@plannotator/opencode@latest"]`

## 사용 명령
```text
/plannotator-annotate README.md
/plannotator-annotate src/
/plannotator-last                     # 에이전트의 마지막 메시지에 주석
/plannotator-review                   # 로컬 변경 리뷰
/plannotator-review <github-pr-url>
plannotator annotate http://localhost:5173
plannotator inbox
```
- Codex에서는 `$plannotator-review`, `$plannotator-annotate`, `$plannotator-last`

## 워크플로 위치
**계획 → 구현 → 검증 루프의 "계획 승인"과 "검증" 단계**에 끼워 쓴다.
- Claude Code: plan mode 종료(`ExitPlanMode`) → hook → 브라우저 UI → 승인 또는 주석 피드백 → 에이전트 수정 → plan diff
- 작업 후 `/plannotator-review`로 PR 스타일 리뷰 → "Send feedback"이 세션으로 돌아감, 승인하면 "LGTM"
→ [plan-implement-verify.md](../09-workflows/development/plan-implement-verify.md), [07-code-review](../07-code-review)

## 응용 아이디어
- 승인된 plan을 Obsidian/Notion에 자동 저장해서 계획 아카이브로 사용 → [09-workflows/logs](../09-workflows/logs)
- 에이전트가 만든 큰 diff를 Guided review로 챕터별 검토
- 에이전트가 만든 HTML/localhost 프로토타입에 직접 주석

## 주의
- 원격(SSH, devcontainer)에서는 서버가 로그인 없이 `0.0.0.0`으로 열리므로 신뢰할 수 없는 네트워크에 포트 노출 금지 (기본 포트 19432)
- 공유 링크는 전체 링크를 아는 사람이 읽을 수 있음. 끄려면 `PLANNOTATOR_SHARE=disabled`, AI 기능 끄기 `PLANNOTATOR_AI=disabled`
