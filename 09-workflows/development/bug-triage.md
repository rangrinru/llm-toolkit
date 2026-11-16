# 버그 처리 흐름

1. **재현**: 재현 단계, 기대/실제 동작, 로그 수집
2. **원인 분석**: [debug.md](../../06-code-fix/debugging/debug.md)로 가설 → 검증
3. **실패하는 테스트 작성**: 버그를 재현하는 테스트 먼저
4. **최소 수정**: [minimal-patch.md](../../06-code-fix/debugging/minimal-patch.md)
5. **검증**: 테스트 통과 + 회귀 확인
6. **기록**: 원인과 해결을 커밋/PR에 남기기
