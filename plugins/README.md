# Plugins & MCP

Claude Code 플러그인, MCP 서버, 에디터 확장 등 **기능 확장** 모음.

## MCP 서버
| 이름 | 용도 | 링크 |
|---|---|---|
| 공식 MCP 서버 모음 | Filesystem, Git, Fetch 등 레퍼런스 서버 | https://github.com/modelcontextprotocol/servers |
| Playwright MCP | 브라우저 자동화 | https://github.com/microsoft/playwright-mcp |
| Context7 | 최신 라이브러리 문서 주입 | https://github.com/upstash/context7 |

## Claude Code 플러그인
| 이름 | 용도 | 링크 |
|---|---|---|
| claude-mem | 세션 간 영속 메모리 (캡처 → 압축 → 다음 세션 주입) | `/plugin marketplace add thedotmack/claude-mem` / [정리](./claude-mem.md) |
| Knowledge Work Plugins | Anthropic 직군별 플러그인 (engineering, design, sales 등 17개+) | `claude plugin marketplace add anthropics/knowledge-work-plugins` / [정리](./knowledge-work-plugins.md) |
| Plannotator | 에이전트 계획/diff 주석 리뷰 | `/plugin marketplace add backnotprop/plannotator` / [정리](../tools/plannotator.md) |
| Hallmark | AI 티 안 나는 웹 디자인 스킬 (`/hallmark`, redesign, audit) | `/plugin marketplace add nutlope/hallmark` → `/plugin install hallmark@hallmark` / [정리](../01-design/hallmark) |

## 설정 예시
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## 참고
- MCP 문서: https://modelcontextprotocol.io
