# Plugins & MCP

Claude Code 플러그인, MCP 서버, 에디터 확장 등 **기능 확장** 모음.

## MCP 서버
| 이름 | 용도 | 링크 |
|---|---|---|
| 공식 MCP 서버 모음 | Filesystem, Git, Fetch 등 레퍼런스 서버 | https://github.com/modelcontextprotocol/servers |
| Playwright MCP | 브라우저 자동화 | https://github.com/microsoft/playwright-mcp |
| Context7 | 최신 라이브러리 문서 주입 | https://github.com/upstash/context7 |

## 플러그인 분석 (다른 레포의 핵심 원리 정리)
| 이름 | 핵심 아이디어 | 정리 문서 |
|---|---|---|
| claude-mem | hook으로 캡처 → observer가 압축 → 인덱스만 주입하고 상세는 필요할 때 (progressive disclosure 메모리) | [claude-mem.md](./claude-mem.md) |
| Knowledge Work Plugins | 직무를 skills/commands/connectors로 분해한 방법론 모음 | [knowledge-work-plugins.md](./knowledge-work-plugins.md) |
| Plannotator | 계획 승인 지점을 가로채 사람의 구조화된 주석을 프롬프트로 되돌림 | [../tools/plannotator.md](../tools/plannotator.md) |
| Hallmark | AI 티를 규칙과 렌더 검사로 막는 디자인 스킬 | [../01-design/hallmark](../01-design/hallmark) |

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
