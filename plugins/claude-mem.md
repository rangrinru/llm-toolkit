# claude-mem 정리 (세션 간 메모리)

> 원본: [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) (Apache-2.0) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+17k stars)

**에이전트가 세션 중에 한 일을 캡처하고 AI로 압축해서, 다음 세션에 관련 맥락을 다시 넣어주는 영속 메모리.** Claude Code, Codex, Cursor, OpenCode, Gemini 등 다수 지원.

## 동작 원리
1. **캡처**: hooks가 모든 tool call(읽기, 편집, 실행)을 로컬 worker로 전달
2. **압축**: 두 번째 에이전트(observer)가 활동을 짧은 observation으로 만들고, 세션 종료 시 summary 작성
3. **주입**: 다음 세션 시작 시 관련 observation의 **압축 인덱스만** 넣고, 상세는 필요할 때 가져옴 (프로젝트 두 번째 세션부터)

사용하는 Claude Code hooks: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, Stop, SubagentStop, SessionEnd

### 3단계 검색 (progressive disclosure)
| 단계 | MCP 도구 | 크기 |
|---|---|---|
| 1 | `search`: ID가 붙은 압축 인덱스 | 결과당 약 50~100 tokens |
| 2 | `timeline`: 특정 항목 주변 시간순 맥락 | - |
| 3 | `get_observations`: 고른 ID의 상세만 (여러 개는 한 번에) | 결과당 약 500~1,000 tokens |

- 저장: SQLite `~/.claude-mem/claude-mem.db` + Chroma 시맨틱 검색 + FTS5 키워드 검색
- 웹 UI: worker URL의 `/viewer`
- `<private>` 태그로 감싼 내용은 저장되지 않음
- `~/.claude-mem/settings.json`의 `CLAUDE_MEM_MODE`: `code`, `code--chill`(기록량 줄임), **`code--ko`(한국어 observation)**

## 설치
```bash
npx claude-mem install          # 설치 후 Claude Code 재시작
npx claude-mem doctor
npx claude-mem telemetry disable
```
```text
# Claude Code 플러그인 마켓플레이스
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```
- 다른 하네스: `npx claude-mem install --ide opencode` (t3code, antigravity, pi 등)
- `npm install -g claude-mem`은 SDK만 설치하고 hooks/worker를 등록하지 않으니 쓰지 말 것
- 수동 학습: `/learn-codebase` (약 5분, 선택)

## 응용 아이디어
- **3단계 검색 패턴**을 개인 문서 정리에도: 목록과 ID만 먼저 훑고, 필요한 문서만 열어 토큰 절약
- **SessionStart에 이전 요약 주입 + Stop/SessionEnd에 요약 저장**하는 hook 설계는 자체 하네스에도 적용 가능 → [hooks 예시](../08-agent-instructions/claude-code/hooks/settings.example.json)
- 민감 정보는 저장 전에 제외하는 규칙(`<private>`)

## 주의
- Node.js 20.19+ 또는 22.12+, Bun과 uv(없으면 자동 설치)
- **비용**: 설치 중 claude-mem 계정 로그인을 요청. "claude-mem observer"를 고르면 30일 무료 체험(결제 수단 필요), 이후 구독하지 않으면 Anthropic 플랜으로 전환. 본인 OpenRouter/Gemini 키나 Anthropic 플랜도 선택 가능. 로그인을 건너뛰려면 `--provider` 또는 `CLAUDE_MEM_ONLINE_OPTIN=false`
- **프라이버시**: 데이터는 로컬(`~/.claude-mem`), Cloud Sync는 opt-in. 익명 통계는 기본 켜짐. observer가 tool 활동을 모델로 보내므로 비밀 정보가 섞일 수 있음. 스크린샷 기본 보관(설정에서 끄기 가능)
- README 끝의 CMEM 토큰 홍보는 기능과 무관
