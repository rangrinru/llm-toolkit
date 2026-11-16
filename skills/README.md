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

## 작성 팁
- `description`은 "언제 이 스킬을 써야 하는지"를 명확하게 (모델이 이걸 보고 로드 여부를 판단)
- SKILL.md 본문은 짧게, 세부 내용은 `references/`로 분리 (progressive disclosure)
- 반복되는 코드는 프롬프트에 넣지 말고 `scripts/`로

## 참고
- Anthropic Skills: https://github.com/anthropics/skills
- Claude Skills 문서: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
