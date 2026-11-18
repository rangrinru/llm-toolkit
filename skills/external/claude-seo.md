# Claude SEO 정리

> 원본: [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) (MIT) | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+11k stars)

**Claude Code용 오픈소스 SEO 감사 플러그인.** 사이트 URL을 주면 10~15분 안에 전체 감사를 하고 우선순위 액션 플랜을 준다. 기술 SEO, Core Web Vitals, E-E-A-T, Schema.org, AI 검색(GEO), 로컬, 이커머스, 국제 SEO까지. 약 26~29개 하위 스킬, 19~20개 서브에이전트(문서마다 수치가 조금 다름).
- 1차 대상: Claude Code 1.0.33+. Cursor, Codex CLI, Gemini CLI, Cline, Aider 등도 `AGENTS.md`로 호환

## 설치
```text
/plugin marketplace add AgriciDaniel/claude-seo
/plugin install claude-seo@agricidaniel-claude-seo
/seo setup        # 자체 Python 환경과 headless 브라우저 설치
/seo doctor       # 상태 점검
```
수동 설치 (README 권장: 스크립트를 파이프로 바로 실행하지 말고 clone 후 검토):
```bash
git clone --depth 1 https://github.com/AgriciDaniel/claude-seo.git
bash claude-seo/install.sh                                         # macOS/Linux
powershell -ExecutionPolicy Bypass -File claude-seo\install.ps1   # Windows
```

## 주요 명령
```text
/seo audit https://example.com      # 최대 17개 에이전트 병렬, Critical~Low 액션 플랜 + MD/PDF/JSON 리포트
/seo page https://example.com/pricing
/seo geo https://example.com        # AI 검색 최적화
/seo schema https://example.com
/seo local https://example.com
```
| 그룹 | 명령 |
|---|---|
| 감사/계획 | `setup`, `doctor`, `audit`, `page`, `plan` |
| 기술 | `technical`, `sitemap`, `images`, `hreflang`, `programmatic`, `google`, `drift` |
| 콘텐츠 | `content`, `content-brief`, `cluster`, `sxo`, `flow`, `competitor-pages` |
| 스키마/AI 검색 | `schema`, `geo`, `agentic`(llms.txt, WebMCP 등) |
| 로컬/링크/커머스 | `local`, `maps`, `backlinks`, `ecommerce` |

- `/seo drift baseline | compare | history <url>`: SEO 변경 모니터링
- 업종(SaaS, local, e-commerce, publisher, agency)을 감지해 점검 항목 조정

## 설치 없이 응용할 분석 원칙 (thinking framework)
1. **관찰과 해석을 분리**: 먼저 수집만 하고(HTML, schema, SERP, CWV, 경쟁 페이지) 점수/분류는 나중에
2. **권고마다 기대는 가정을 드러내기** (예: "홈페이지가 사이트 대표"라는 가정)
3. **실제 검색 결과(SERP)가 우선**: 권고가 같은 의도의 SERP와 모순되면 SERP를 따름. 커뮤니티 주장보다 Google 1차 문서
4. **병목부터**: 색인 불가, LCP, canonical처럼 나머지를 막는 결함 하나를 먼저
5. **교차 확인**: 여러 점검 결과를 겹쳐 보고 증상과 원인을 구분
6. **액션 플랜은 의존성 그래프로**: 가장 많은 것을 풀어주는 것, 순서가 있는 것, 병렬 가능한 것을 구분
→ 이 원칙은 SEO 외 분석 보고서에도 적용 가능: [03-documents/writing/report.md](../../03-documents/writing/report.md)

## 주의
- Python 3.11~3.14 필요. API 키 불필요하지만, Google 무료 API(PageSpeed, CrUX, Search Console, GA4)를 `/seo google setup`으로 연결하면 실측 데이터 사용
- 일부 확장(SE Ranking, DataForSEO 등)은 유료 서비스 계정 필요
- 전체 감사는 Opus 에이전트 5개 등 병렬 에이전트가 많아 **Claude 사용량이 크다**
- 분석하는 페이지 내용은 Claude로 전송됨
