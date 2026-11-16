# PR 리뷰

> 대상 모델: Claude Code, Codex, GPT | 마지막 테스트: YYYY-MM-DD

## 언제 쓰나
- 다른 사람의 PR 또는 에이전트가 만든 변경을 리뷰할 때

## 프롬프트
```text
아래 PR(diff)을 시니어 엔지니어 관점에서 리뷰해줘.

[PR 목적] {설명}

우선순위: 1) 버그/보안 2) 요구사항 충족 여부 3) 성능 4) 가독성/구조 5) 테스트
출력 형식:
- [Blocker / Should fix / Nit] 파일:라인 - 문제 - 수정 제안 코드
- 문제가 없으면 억지로 지적하지 말 것
- 마지막에 Approve / Request changes 의견과 이유

{diff}
```

## 메모
- 
