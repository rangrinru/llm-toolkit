# HWPX 구조와 수정 레시피

HWPX 는 ZIP 안에 XML 이 든 형식이다. 아래는 실제 문서를 고치며 확인한 것만 적었다.

## 파일 구성

| 경로 | 내용 |
|---|---|
| `Contents/header.xml` | 글꼴(`hh:fontface`), 글자 모양(`hh:charPr`), 문단 모양(`hh:paraPr`), 테두리/배경(`hh:borderFill`) 목록 |
| `Contents/section0.xml` | 본문. 문단 `hp:p` → 글자 묶음 `hp:run` → 글 `hp:t`. 표·그림도 문단 안에 들어 있다 |
| `BinData/imageN.png` 등 | 그림 파일. 본문은 `binaryItemIDRef="imageN"` 으로 가리킨다 |
| `Preview/PrvText.txt`, `PrvImage.png` | 미리보기. 고치지 않아도 열린다 |

- 다시 묶을 때는 원래 ZIP 항목 순서와 압축 방식(`mimetype` 은 무압축)을 그대로 지킨다: `zo.writestr(info, data, compress_type=info.compress_type)`.
- 단위 HWPUNIT: 1 mm ≈ 283.46, 1 pt = 100. A4 폭 59528.
- 글자 크기 `charPr height="1000"` = 10 pt. 자간 `hh:spacing hangul="-3"` = -3 %.

## 서식의 특성 (정부 보고서 서식에서 본 것)

- 본문 전체가 **큰 틀 표의 칸 안**에 들어 있는 경우가 많다. 그래서 문단 모양의 "다음 문단과 함께"(`keepWithNext`) 같은 쪽 나눔 설정이 듣지 않았다.
- 표 대부분은 `hp:pos treatAsChar="1"`(글자처럼 취급)이라 문단 안에 한 글자처럼 놓인다.
- 표 제목 `<표 N>` 은 원래 표 바로 앞의 독립 문단이다(`&lt;표 N&gt;` 로 이스케이프되어 저장됨).

## 문단 모양 (paraPr)

```xml
<hh:paraPr id="90" ...>
  <hh:align horizontal="JUSTIFY" vertical="BASELINE"/>
  <hh:breakSetting breakLatinWord="KEEP_WORD" breakNonLatinWord="KEEP_WORD" keepWithNext="0" .../>
  <hp:switch>
    <hp:case hp:required-namespace="...HwpUnitChar">
      <hh:margin><hc:intent value="-1600"/> ...</hh:margin>      ← 한 벌
    </hp:case>
    <hp:default>
      <hh:margin><hc:intent value="-3200"/> ...</hh:margin>      ← 또 한 벌 (값이 2배)
    </hp:default>
  </hp:switch>
</hh:paraPr>
```

- `intent` 음수 = 내어쓰기(둘째 줄부터 들어감). 글머리표(◦ - ※ ①)가 없는 문단에 걸려 있으면 줄 앞이 비어 보인다.
- **두 벌을 다 고쳐야 한다.** 한 벌만 0 으로 바꿨더니 한글 화면은 그대로였다.
- 복제: `<hh:paraProperties itemCnt="N">` 이 다음 id. 블록을 복사해 id 를 N 으로 바꾸고 끝에 붙인 뒤 itemCnt 를 N+1 로. (`hwpx_patch.Hwpx.clone`)

## 글자 바꾸기

```python
doc = Hwpx('in.hwpx')
doc.replace_text('옛 글', '새 글', count=1)   # 등장 횟수가 다르면 멈춘다
doc.strip_lineseg()
doc.save('out.hwpx', allow_text_change=True)
```
- 같은 글이 여러 곳에 있으면(표 머리칸 이름 등) 문서 순서대로 n 번째를 골라 바꾼다. 어느 표인지는 앞의 `<표 N>` 제목 위치로 범위를 잡는다.
- 숫자 하나를 바꿀 때도 같은 숫자가 다른 뜻으로 쓰인 곳(검증값과 시험값처럼)이 있는지 먼저 전부 찾아보고 고칠 곳만 고른다.

## 표

- 구조: `hp:tbl rowCnt colCnt` > `hp:sz`(전체 폭) > `hp:tr` > `hp:tc` > `hp:subList`(칸 안 문단) + `hp:cellAddr colAddr rowAddr` + `hp:cellSpan colSpan rowSpan` + `hp:cellSz width height` + `hp:cellMargin`.
- 칸 글 너비 = `cellSz width` − 좌우 여백 (`hasMargin="1"` 이면 칸의 `cellMargin`, 아니면 표의 `inMargin`).
- **표 추가**: 비슷한 기존 표(앞 제목 문단 + 표 문단)를 복사해 글만 바꾼다. 행/열을 줄일 땐 해당 `hp:tc` 를 지우고 `cellAddr`, `rowCnt/colCnt`, `hp:sz height`, 남은 칸 `cellSz width` 를 맞춘다. 표 `id` 는 새로(`new_object_id`).
- **열 분리**(2열 → 3열): 나눌 칸을 복제해 `colAddr` 를 하나씩 밀고, 두 칸 폭의 합이 원래 칸 폭이 되게 `cellSz width` 를 나눈 뒤 `colCnt` +1.
- **열 너비 조정**: 같은 열의 모든 칸 `cellSz width` 를 함께 바꾸고, 표 전체 폭(`hp:sz width`)은 유지되게 다른 열에서 뺀다. 병합 칸은 걸친 열 폭의 합.
- **행 높이 줄이기**: `cellMargin top/bottom` 을 줄이고(예: 113 → 28) `cellSz height` 도 같은 만큼. 높이는 최소값이라 글이 많으면 한글이 늘린다.
- **표 제목이 다음 쪽으로 갈라짐**: 제목 문단을 표의 `hp:caption side="TOP"` 안으로 옮긴다(`hwpx_patch.py caption`). `keepWithNext` 는 틀 표 안에서 효과 없었다.

```xml
<hp:tbl ...><hp:sz .../><hp:pos .../><hp:outMargin .../>
  <hp:caption side="TOP" fullSz="0" width="8504" gap="283" lastWidth="표 폭">
    <hp:subList ...>  (원래 제목 문단 그대로)  </hp:subList>
  </hp:caption>
  <hp:inMargin .../> <hp:tr> ...
```

## 그림

- 구조: `hp:pic` > `hp:sz`, `hp:orgSz`, `hp:curSz`, `hp:imgRect`(pt0~pt3), `hp:imgClip`, `hp:imgDim`, `hc:img binaryItemIDRef`.
- **교체**: `BinData/imageN.*` 파일 내용만 바꾸고, 새 그림 비율에 맞춰 `sz/orgSz height`, `imgRect` y 값, `imgClip`/`imgDim`(원본 픽셀 × 75 정도)을 고친다. 폭은 그대로 두면 배치가 덜 흔들린다.
- **HWP 안의 그림 꺼내기**: OLE `BinData/BIN0001.bmp` 등, 압축 문서면 `zlib.decompress(raw, -15)`. (`hwp_tools.py images`)
- **삭제**: 그림이 든 문단과 그 아래 캡션 문단 `[그림 N] …` 을 함께 지운다. 그 그림 파일을 다른 곳이 쓰는지 `binaryItemIDRef` 로 확인.
- **번호 당기기**: 캡션 `[그림 N]` 을 N−1 로. 본문에서 "그림 N" 을 언급한 곳이 있는지도 찾아 같이 바꾼다.

## HWP(5.x 바이너리)

- OLE 파일. `FileHeader` 36 바이트째 bit0 = 압축 여부. 본문 `BodyText/SectionN` 은 raw deflate.
- 레코드 머리 4 바이트: tag = 하위 10 bit, size = 상위 12 bit(0xfff 면 다음 4 바이트가 크기). 문단 글은 tag 67, UTF-16LE. 조판 부호 1·2·3·11~18·21~23 은 16 바이트를 건너뛴다. (`hwp_tools.py text`)
- 쓰기는 하지 않는다. `python-hwpx` 의 `HwpxDocument.open('x.hwp')` → `save_to_path('x.hwpx')` 로 바꾼 뒤 고치고, 사용자가 한글에서 HWP 로 다시 저장한다. 변환 보고서(`conversion_report`)의 빠진 항목과 표·그림 개수를 확인한다.

## 저장 전 검사 목록

- [ ] 글 내용: 서식만 고쳤으면 태그를 뺀 글이 원본과 같은가
- [ ] 표·그림·캡션 개수가 예상대로인가
- [ ] `hwpx.validate_editor_open_safety(out).ok`
- [ ] 줄 배치 캐시를 지웠는가(글·표를 바꿨을 때)
- [ ] 대상 파일이 작업 시작 때와 같은가(`cmp`) — 다르면 사용자가 그 사이 저장한 것
