# 오피스 파일 생성 / 변환

> 대상 모델: Claude (Skills), GPT (Code Interpreter) | 마지막 테스트: YYYY-MM-DD

## 언제 쓰나
- PPTX, DOCX, XLSX를 생성하거나 변환할 때

## 프롬프트
```text
{입력 자료}를 바탕으로 {DOCX / PPTX / XLSX} 파일을 만들어줘.

- 구조: {목차 / 시트 구성 / 슬라이드 수}
- 스타일: {폰트, 색상, 템플릿}
- 표/차트가 필요한 부분: {설명}

python-docx / python-pptx / openpyxl 등을 사용하고, 생성 후 내용을 검증해줘.
```

## 메모
- HWP는 직접 생성이 어려우므로 DOCX로 만든 뒤 한글에서 변환하는 방식 권장
