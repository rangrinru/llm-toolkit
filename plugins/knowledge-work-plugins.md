# Knowledge Work Plugins 정리 (Anthropic)

> 원본: [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (Apache-2.0) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+6.5k stars)

**직군별로 Claude를 전문가로 바꾸는 파일 기반 플러그인 모음.** skills, connectors(MCP), slash commands, 서브에이전트를 직무 단위로 묶었다. 주 대상은 Claude Cowork이고 Claude Code에서도 사용 가능. 전부 markdown과 JSON이라 코드/빌드가 필요 없다.

## 설치 (Claude Code)
```bash
claude plugin marketplace add anthropics/knowledge-work-plugins
claude plugin install sales@knowledge-work-plugins
```
- Cowork에서는 claude.com/plugins에서 설치
- 사용 예: `/sales:call-prep`, `/data:write-query`, `/finance:reconciliation`, `/product-management:write-spec`

## 플러그인 목록
| 플러그인 | 내용 | 이 레포 관련 카테고리 |
|---|---|---|
| `productivity` | 태스크 관리, 일정 계획, 업무 맥락 메모리 | [09-workflows](../09-workflows) |
| `product-management` | 기능 스펙, 로드맵, 사용자 리서치 종합, 이해관계자 업데이트 | [03-documents](../03-documents) |
| `engineering` | 스탠드업, code-review, architecture, debug, deploy-checklist, incident-response, tech-debt, testing-strategy | [05](../05-code-inspection) / [06](../06-code-fix) / [07](../07-code-review) |
| `design` | design-critique, design-system, ux-copy, accessibility-review, design-handoff, research-synthesis | [01-design](../01-design) |
| `marketing` | 콘텐츠 제작, 캠페인 기획, 브랜드 보이스, 경쟁사 브리핑 | 03-documents |
| `data` | SQL 작성, 데이터 탐색, 시각화/대시보드 | - |
| `sales` | 콜 준비/요약, 계정 리서치, 딜/파이프라인 리뷰, 포캐스트 (36개 스킬) | - |
| `customer-support` | 티켓 분류, 답변 초안, 에스컬레이션, KB 문서화 | 03-documents |
| `legal` | 계약 검토, NDA 분류, 컴플라이언스, 법률 브리프 | - |
| `finance` | 분개, 계정 조정, 재무제표, 월마감 | - |
| `human-resources` | 채용, 온보딩, 성과 평가, 보상 분석 | - |
| `operations` | 벤더 관리, 프로세스 문서화, runbook, 리스크 평가 | 09-workflows |
| `enterprise-search` | 이메일/채팅/문서/위키 통합 검색 | - |
| `small-business` | 소상공인용 (인보이스, 급여, 세금 등. 돈/고객 관련 단계는 사용자 승인) | - |
| `bio-research` | 전임상 연구 도구/DB 연결 | - |
| `pdf-viewer` | PDF 열람, 주석, 서명, 양식 작성 | 03-documents |
| `cowork-plugin-management` | 조직에 맞는 플러그인 생성/커스터마이즈, MCP 설정 | [plugins](.) |
| `partner-built/` | apollo, brand-voice, common-room, slack, zoom-plugin | - |

## 플러그인 구조 (내 플러그인 만들 때 참고)
```
plugin-name/
├── .claude-plugin/plugin.json   # 매니페스트
├── .mcp.json                    # 외부 도구 연결 (MCP)
├── commands/                    # 직접 부르는 슬래시 명령
└── skills/                      # 관련될 때 자동으로 쓰는 도메인 지식
```

## 응용 아이디어
- 내 직무/작업 흐름을 `skills/<name>/SKILL.md` 단위로 쪼개 마켓플레이스 형태로 관리
- `.mcp.json`의 connector만 바꿔 같은 스킬을 다른 도구 스택(Slack/Notion/Jira 등)에서 사용
- 회사 용어, 조직, 프로세스를 스킬 파일에 넣어 맥락 고정
- `engineering`, `design` 플러그인의 스킬 이름은 이 레포 05~07, 01 카테고리 구성과 거의 같아서 비교 참고용으로 좋음

## 주의
- connector는 외부 서비스 계정과 인증 필요 (비용 별도)
- sales 등은 요청 시 CRM 수정, 이메일 발송, 미팅 예약까지 할 수 있으니 쓰기 권한 범위 확인
- 범용 출발점이라 실제 사용 전 수정 필요. 법률/재무/인사 결과물은 전문가 검토 필요
