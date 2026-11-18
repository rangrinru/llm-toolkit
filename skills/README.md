# Skills

Claude Skills(`SKILL.md`), Codex/에이전트용 재사용 가능한 **작업 지침 패키지** 모음.

## 구조
```
skills/
├── _template/SKILL.md     # 새 스킬 작성용 템플릿
└── <skill-name>/
    ├── SKILL.md           # 필수: 이름, 설명, 워크플로우
    ├── scripts/           # 선택: 실행 스크립트
    ├── references/        # 선택: 참고 문서
    └── assets/            # 선택: 템플릿, 이미지
```

## 스킬 목록
| 스킬 | 설명 |
|---|---|
| [`hwpx-formatting`](./hwpx-formatting/SKILL.md) | 한글(HWP/HWPX) 문서를 한글 프로그램 없이 고치기: 글 겹침, 띄어쓰기 벌어짐, 끝줄 한 글자, 표 제목 갈라짐, 열 너비 |
| [`natural-korean-writing`](./natural-korean-writing/SKILL.md) | 자연스러운 한국어 문장 작성 및 교정: 번역투 조사 제거, 용언 중심 서술, 단문화, 종결어미 변주 및 AI Slop 박멸 |

## 외부 스킬 분석 (다른 레포의 핵심 원리 정리)
설치법이 아니라 각 스킬이 **어떤 방법론과 알고리즘으로 동작하는지**를 정리한 문서.

| 스킬 | 핵심 아이디어 | 정리 문서 |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | progressive disclosure, description이 트리거, 스킬 작성/평가 루프(skill-creator)와 스킬 19개의 방법론 | [external/anthropic-skills.md](./external/anthropic-skills.md) |
| [Cloudflare security-audit-skill](https://github.com/cloudflare/security-audit-skill) | coverage ledger 기반 헌팅, 찾는 에이전트와 반증하는 에이전트 분리, 3단계 판정 | [05-code-inspection](../05-code-inspection/security/cloudflare-security-audit-skill.md) |
| [Hallmark](https://github.com/Nutlope/hallmark) | 바닥 규칙 + 테마 deal + 렌더 린트 + 새 컨텍스트 리뷰 | [01-design/hallmark](../01-design/hallmark) |
| [Impeccable](https://github.com/pbakaus/impeccable) | 디자인 명령어 어휘, PRODUCT/DESIGN 컨텍스트, 결정적 slop 감지 규칙 62개 | [01-design/impeccable](../01-design/impeccable) |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | 업종 분류 → 취향 대신 deal → 다중 폭 gate | [01-design/taste-skill](../01-design/taste-skill) |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | 시간의 함수로서의 화면, 프레임 단위 seek 캡처로 결정적 렌더 | [02-motion-graphics/hyperframes](../02-motion-graphics/hyperframes) |
| [Claude SEO](https://github.com/AgriciDaniel/claude-seo) | 관찰과 해석 분리, 10원칙 사고 프레임워크, 점수 산정과 품질 게이트 | [external/claude-seo.md](./external/claude-seo.md) |

## 작성 팁
- `description`은 "언제 이 스킬을 써야 하는지"를 명확하게 (모델이 이걸 보고 로드 여부를 판단)
- SKILL.md 본문은 짧게, 세부 내용은 `references/`로 분리 (progressive disclosure)
- 반복되는 코드는 프롬프트에 넣지 말고 `scripts/`로

## 참고
- Anthropic Skills: https://github.com/anthropics/skills
- Claude Skills 문서: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
