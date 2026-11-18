# DeepTutor 정리

> 원본: [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) (Apache-2.0, 홍콩대 HKUDS) | 홈페이지: https://deeptutor.info | 정리일: 2026-11-18 | GitHub 월간 트렌딩 (+18k stars)

**"평생 개인화 튜터링."** 튜터링, 리서치, 콘텐츠 생성, 연습 문제를 하나의 런타임으로 묶은 에이전트 기반 학습 워크스페이스. 코딩 에이전트 워크플로가 아니라 **공부와 리서치용 독립 앱**.

## 핵심 기능
- 모드: Chat, Quiz, Research, Visualize, Solve, Mastery Path, Reading이 세션 맥락을 공유
- 지식베이스: 문서/영상/오디오를 LlamaIndex, GraphRAG, LightRAG 등으로 인덱싱하고 출처 인용
- 검사 가능한 메모리: L1 traces, L2 facts, L3 synthesis를 Memory Graph에서 근거와 함께 확인/편집
- 도구: `web_search`, `paper_search`, `zotero_search`, `reason`, `geogebra_analysis`, 이미지/영상 생성, Manim 수학 애니메이션
- Claude Code, Codex 등을 "상담 에이전트"로 호출 가능, 반대로 다른 에이전트가 DeepTutor CLI를 도구로 사용 가능

## 설치
```bash
# PyPI (Web 앱 + CLI), Python 3.11~3.14 / Node.js 20.9+
python -m pip install -U "deeptutor[full]"
deeptutor init     # 포트, LLM provider, 임베딩/검색 설정
deeptutor start    # http://127.0.0.1:3782

# CLI 전용
python -m pip install -U deeptutor
deeptutor init --cli
deeptutor chat
```
- Docker: `ghcr.io/hkuds/deeptutor:latest` (포트 3782)
- 데스크톱 앱(macOS, Windows preview)도 있음. 한국어 UI는 preview

## CLI 예시
```bash
deeptutor run deep_research "Survey 2026 papers on RAG" --config mode=report --config depth=standard
deeptutor run deep_solve "Find d/dx[sin(x^2)]" --tool reason --format json
deeptutor run math_animator "Animate a sine wave" --config enable_visual_review=true
```
- `--format json`은 NDJSON 이벤트 스트림 → 다른 에이전트의 도구로 쓰기 좋음 (레포 루트 `SKILL.md` 제공)

## 응용 아이디어
- 자료 PDF를 지식베이스로 만들고 `deep_research`로 서베이 → 같은 세션으로 퀴즈까지 → [09-workflows/research](../09-workflows/research)
- `math_animator`(Manim) 기능은 [02-motion-graphics/manim](../02-motion-graphics/manim)과 연결

## 주의
- LLM provider 설정 필수(API 비용은 provider 기준). 인덱싱, 영상 생성, 시각 검수는 추가 호출 비용
- Windows 데스크톱 빌드는 서명되지 않아 SmartScreen 경고
