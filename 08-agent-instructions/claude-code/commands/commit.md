---
description: 현재 변경사항을 확인하고 Conventional Commit 메시지로 커밋
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*)
---

1. git status와 git diff로 변경사항을 확인한다.
2. 관련 없는 변경이 섞여 있으면 논리 단위로 나눠 커밋한다.
3. 메시지 형식: type(scope): 요약 (feat, fix, docs, refactor, test, chore)
4. 커밋 후 결과를 요약한다.

추가 지시: $ARGUMENTS
