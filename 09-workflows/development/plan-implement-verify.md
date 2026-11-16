# 계획 → 구현 → 검증 기본 루프

에이전트에게 코드 작업을 맡길 때의 기본 흐름.

## 1. 탐색 (Explore)
```text
관련 파일을 읽고 현재 구조를 파악해줘. 아직 코드는 수정하지 마.
```

## 2. 계획 (Plan)
```text
{목표}를 위한 구현 계획을 단계별로 세워줘. 변경할 파일, 위험 요소, 테스트 방법을 포함해.
```
- 계획을 검토하고 수정 요청 후 승인

## 3. 구현 (Implement)
```text
계획대로 1단계부터 구현해. 각 단계 후 테스트를 실행하고 결과를 알려줘.
```

## 4. 검증 (Verify)
- [셀프 리뷰](../../07-code-review/self-review/self-review.md)
- 테스트/린트/타입체크 통과 확인

## 5. 마무리
- 커밋, PR 설명 작성
- 배운 점은 [CLAUDE.md](../../08-agent-instructions/claude-code/CLAUDE.md.template)에 반영
