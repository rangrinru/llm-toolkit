"""HWP(5.x 바이너리) 파일 다루기: 글 뽑기, 그림 꺼내기, HWPX 로 바꾸기.

한글 프로그램이 없는 PC 에서도 동작한다. HWP 바이너리에 직접 쓰는 것은 안 되므로,
고칠 때는 HWPX 로 바꾼 사본을 고치고 한글에서 열어 'HWP 로 다른 이름 저장'한다.

사용법
    python hwp_tools.py text    문서.hwp  [결과.txt]     # 본문 글을 문단마다 한 줄로
    python hwp_tools.py images  문서.hwp  폴더/          # BinData 의 그림을 파일로
    python hwp_tools.py convert 문서.hwp  결과.hwpx      # python-hwpx 로 HWPX 변환 + 열기 검사
"""
import io
import os
import struct
import sys
import zlib

import olefile

# 문단 글(HWPTAG_PARA_TEXT) 안에서 8 글자(16 바이트) 크기로 들어 있는 조판 부호들
EXTENDED_CTRL = {1, 2, 3, 11, 12, 14, 15, 16, 17, 18, 21, 22, 23}


def _compressed(ole):
    return ole.openstream('FileHeader').read()[36] & 1


def text(path):
    ole = olefile.OleFileIO(path)
    comp = _compressed(ole)
    secs = sorted((s for s in ole.listdir() if s[0] == 'BodyText'), key=lambda s: int(s[1][7:]))
    out = []
    for s in secs:
        data = ole.openstream(s).read()
        if comp:
            data = zlib.decompress(data, -15)
        i = 0
        while i < len(data):
            h = struct.unpack('<I', data[i:i + 4])[0]
            i += 4
            tag, size = h & 0x3ff, (h >> 20) & 0xfff
            if size == 0xfff:
                size = struct.unpack('<I', data[i:i + 4])[0]
                i += 4
            if tag == 67:                                   # HWPTAG_PARA_TEXT
                b, j, chars = data[i:i + size], 0, []
                while j + 1 < len(b):
                    c = struct.unpack('<H', b[j:j + 2])[0]
                    if c in EXTENDED_CTRL:
                        j += 16
                        continue
                    if c >= 32:
                        chars.append(chr(c))
                    elif c == 9:
                        chars.append('\t')
                    j += 2
                t = ''.join(chars).strip()
                if t:
                    out.append(t)
            i += size
    return out


def images(path, folder):
    """BinData 스트림을 꺼낸다. 압축된 문서는 raw deflate(zlib -15)로 풀어야 한다."""
    ole = olefile.OleFileIO(path)
    os.makedirs(folder, exist_ok=True)
    names = []
    for s in ole.listdir():
        if s[0] != 'BinData':
            continue
        raw = ole.openstream(s).read()
        try:
            data = zlib.decompress(raw, -15)
        except zlib.error:
            data = raw
        fn = os.path.join(folder, s[1])
        with open(fn, 'wb') as f:
            f.write(data)
        names.append(fn)
    return names


def convert(path, out):
    import hwpx
    from hwpx.document import HwpxDocument
    doc = HwpxDocument.open(path)
    rep = getattr(doc, 'conversion_report', None)
    if rep is not None and (rep.unconverted or rep.dropped):
        print('변환 중 빠진 것:', dict(rep.unconverted), dict(rep.dropped))
    doc.save_to_path(out)
    r = hwpx.validate_editor_open_safety(out)
    assert r.ok, r.summary
    return out


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, src = sys.argv[1], sys.argv[2]
    dst = sys.argv[3] if len(sys.argv) > 3 else None
    if cmd == 'text':
        lines = text(src)
        if dst:
            with open(dst, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
        else:
            print('\n'.join(lines))
    elif cmd == 'images':
        for n in images(src, dst or 'bindata'):
            print(n)
    elif cmd == 'convert':
        print('저장', convert(src, dst))
    else:
        sys.exit(__doc__)
