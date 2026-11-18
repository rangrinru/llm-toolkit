# anthropics/skills 정리 (공식 Agent Skills)

> 원본: [anthropics/skills](https://github.com/anthropics/skills) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+15k stars, 누적 약 197k)
> 라이선스: 스킬별로 다름 (docx, pdf, pptx, xlsx 등 다수 Apache-2.0, 각 폴더의 LICENSE.txt 확인)

Anthropic의 **Agent Skills 공식 예제 저장소**. 스킬은 `SKILL.md` 하나가 필수인 폴더이고, Claude가 필요할 때 동적으로 로드한다. 스펙은 https://agentskills.io/specification 으로 이전됨. 시연/교육용이라 실제 Claude 동작과 다를 수 있으니 중요한 작업 전에 직접 테스트할 것.

## 설치 (Claude Code)
```text
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```
- 호출: 스킬 이름을 언급. 예: *Use the PDF skill to extract the form fields from path/to/some-file.pdf*
- Claude.ai: 유료 플랜에 기본 탑재, 설정에서 업로드 가능 / API: Skills API

## 스킬 목록 (19개)
| 스킬 | 설명 | 이 레포에서 관련 카테고리 |
|---|---|---|
| `docx` | Word 생성, 읽기, 편집 | [03-documents](../../03-documents) |
| `pdf` | PDF 읽기, 병합, 분할, 폼 작성, OCR 등 | 03-documents |
| `pptx` | PowerPoint 생성, 읽기, 편집 | 03-documents, [01-design/slides](../../01-design/slides) |
| `xlsx` | 엑셀/CSV 읽기, 편집, 수식, 차트 | 03-documents |
| `doc-coauthoring` | 문서, 제안서, 스펙 공동 작성 워크플로 | 03-documents |
| `internal-comms` | 상태 보고, 리더십 업데이트, 뉴스레터, 사고 보고 | 03-documents |
| `frontend-design` | 템플릿스럽지 않은 UI 디자인 가이드 | [01-design](../../01-design) |
| `canvas-design` | 포스터, 아트 등 정적 비주얼(.png/.pdf) | 01-design |
| `theme-factory` | 슬라이드, 문서, 랜딩에 프리셋 10개 또는 즉석 테마 적용 | 01-design |
| `brand-guidelines` | Anthropic 브랜드 색상/타이포 적용 (자기 브랜드용으로 변형 가능) | 01-design |
| `algorithmic-art` | p5.js 제너러티브 아트 | 01-design, [02-motion-graphics](../../02-motion-graphics) |
| `slack-gif-creator` | Slack용 애니메이션 GIF | 02-motion-graphics |
| `web-artifacts-builder` | React, Tailwind, shadcn/ui로 복합 HTML artifact | 01-design |
| `webapp-testing` | Playwright로 로컬 웹앱 테스트, 스크린샷 | [05-code-inspection](../../05-code-inspection) |
| `mcp-builder` | MCP 서버 제작 가이드 (Python FastMCP / TypeScript SDK) | [plugins](../../plugins) |
| `claude-api` | Claude API/SDK 레퍼런스 | tools |
| `skill-creator` | 스킬 생성, 개선, eval, description 트리거 최적화 | [skills](..) |
| `discernment-nudge` | 답변 뒤에 사실/추론/누락 맥락을 점검하는 후속 질문 2~3개 추가 | [04-context-editing](../../04-context-editing) |
| `academy-guide` | Claude 사용법 질문에 Claude Academy 강의 추천 | - |

플러그인 묶음: `document-skills` = xlsx, docx, pptx, pdf / `example-skills` = 나머지 예제들

## 스킬 작성 원칙 (내 스킬 만들 때)
1. **description이 트리거**: "무엇을 하는가 + 언제 쓰는가(구체적 키워드, 상황)"를 모두 description에. "when to use"는 본문이 아니라 description에 둔다. Claude는 덜 호출하는 경향이 있으니 description을 적극적으로 쓴다
2. **frontmatter 필수 필드는 `name`(소문자-하이픈)과 `description` 두 개뿐**
3. **SKILL.md는 짧게**, 상세는 `references/`로 분리 (예: pdf 스킬의 FORMS.md, REFERENCE.md)
4. **작성 루프 (skill-creator)**: 의도 파악 → 인터뷰/조사 → 초안 → 테스트 프롬프트 실행 → 평가 → 재작성 반복 → 마지막에 description 최적화
5. **워크플로형 스킬**은 단계 구조로 (doc-coauthoring: 맥락 전달 → 반복 다듬기 → 독자 검증)
6. **discernment-nudge 패턴**: 행동에 옮길 답변에는 사실, 추론, 누락 맥락을 점검하는 후속 질문 2~3개를 붙인다

→ 내 스킬 템플릿: [skills/_template/SKILL.md](../_template/SKILL.md)
