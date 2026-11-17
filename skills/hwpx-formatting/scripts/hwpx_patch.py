"""HWPX 서식 패치 도구. XML 을 문자열 그대로 고쳐서 손대지 않은 부분은 바이트까지 보존한다.

명령
    python hwpx_patch.py stats    문서.hwpx
    python hwpx_patch.py relayout 문서.hwpx 결과.hwpx           # 줄 배치 캐시 전체 삭제(글 겹침 해결)
    python hwpx_patch.py replace  문서.hwpx 결과.hwpx --old "옛 글" --new "새 글" [--count N]
    python hwpx_patch.py caption  문서.hwpx 결과.hwpx [--pattern "&lt;표 [\\d-]+&gt;"]
                                                               # 표 제목 문단을 표의 위쪽 캡션으로 옮김

라이브러리로 쓰기
    from hwpx_patch import Hwpx, edit_align, edit_intent_zero, edit_spacing
    doc = Hwpx('in.hwpx')
    new_id = doc.clone('paraPr', '90', edit_align('LEFT'))     # 문단 모양 90 을 복제해 왼쪽 맞춤으로
    doc.set_para_pr(paragraph_xml_fragment, new_id)            # 또는 문자열 치환으로 paraPrIDRef 교체
    doc.strip_lineseg()
    doc.save('out.hwpx')                                       # 글 내용이 바뀌었으면 저장을 거부
"""
import argparse
import io
import random
import re
import sys
import zipfile

SECTION = re.compile(r'Contents/section\d+\.xml$')
GROUP = {'paraPr': 'paraProperties', 'charPr': 'charProperties', 'borderFill': 'borderFills'}


class Hwpx:
    def __init__(self, path):
        self.path = path
        self.z = zipfile.ZipFile(path)
        self.header = self.z.read('Contents/header.xml').decode('utf-8')
        self.secs = {n: self.z.read(n).decode('utf-8') for n in self.z.namelist() if SECTION.match(n)}
        self.bins = {}                       # 바꿀 BinData: {'BinData/image3.png': bytes}
        self._text0 = self.plain()

    # ---------- 읽기 ----------
    def plain(self):
        """태그를 뺀 글 전체. 서식만 고쳤는지 확인할 때 쓴다."""
        return ''.join(re.sub(r'<[^>]+>', '', s) for _, s in sorted(self.secs.items()))

    def block(self, kind, id_):
        return re.search(r'<hh:%s id="%s".*?</hh:%s>' % (kind, id_, kind), self.header, re.S).group(0)

    # ---------- 문단·글자 모양 ----------
    def clone(self, kind, src_id, edit):
        """header.xml 의 모양(paraPr/charPr/borderFill)을 복제해 edit(블록 문자열)로 고치고 새 id 를 돌려준다.
        여러 문단이 같은 모양을 함께 쓰므로, 원래 모양을 고치면 엉뚱한 곳까지 바뀐다 → 항상 복제한다."""
        grp = GROUP[kind]
        blk = self.block(kind, src_id)
        m = re.search(r'<hh:%s itemCnt="(\d+)"' % grp, self.header)
        new_id = int(m.group(1))
        assert f'<hh:{kind} id="{new_id}"' not in self.header, 'itemCnt 와 마지막 id 가 맞지 않음'
        nb = edit(blk.replace(f'<hh:{kind} id="{src_id}"', f'<hh:{kind} id="{new_id}"', 1))
        assert nb != blk.replace(f'id="{src_id}"', f'id="{new_id}"', 1), 'edit 가 아무것도 바꾸지 않음'
        end = self.header.find(f'</hh:{grp}>')
        self.header = self.header[:end] + nb + self.header[end:]
        self.header = self.header.replace(m.group(0), f'<hh:{grp} itemCnt="{new_id + 1}"', 1)
        return str(new_id)

    # ---------- 본문 ----------
    def strip_lineseg(self):
        """<hp:linesegarray>(줄 배치 캐시)를 모두 지운다. 한글이 열 때 배치를 다시 계산한다.
        글을 늘리거나 표를 넣은 뒤 이걸 안 하면, 바뀐 문단 뒤의 글이 옛 위치에 그려져 겹친다."""
        n = 0
        for k, s in self.secs.items():
            self.secs[k], c = re.subn(r'<hp:linesegarray>.*?</hp:linesegarray>', '', s, flags=re.S)
            n += c
        return n

    def replace_text(self, old, new, count=1):
        """<hp:t> 안의 글을 바꾼다. 등장 횟수가 count 와 다르면 멈춘다(엉뚱한 곳을 고치지 않게)."""
        pat = re.compile(r'(<hp:t>[^<]*?)' + re.escape(old))
        hits = sum(len(pat.findall(s)) for s in self.secs.values())
        assert hits == count, f'"{old}" 등장 {hits}회 (예상 {count}회)'
        for k, s in self.secs.items():
            self.secs[k] = pat.sub(lambda m: m.group(1) + new, s)
        return hits

    def table_title_to_caption(self, pattern=r'&lt;표 [\d-]+&gt;', gap=283):
        """'<표 N> 제목' 문단을 바로 뒤 표의 위쪽 캡션(hp:caption side=TOP)으로 옮긴다.
        본문이 큰 표의 칸 안에 들어 있는 서식에서는 '다음 문단과 함께'(keepWithNext)가 듣지 않아
        제목과 표가 쪽으로 갈라지는데, 캡션은 표의 일부라 갈라질 수 없다."""
        sub = ('<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="TOP" '
               'linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">')
        moved = []
        for k in self.secs:
            x, pos = self.secs[k], 0
            while True:
                m = re.compile(r'<hp:p [^>]*>(?:(?!<hp:p ).)*?<hp:t>\s*' + pattern, re.S).search(x, pos)
                if not m:
                    break
                ps, pe = m.start(), x.find('</hp:p>', m.start()) + 7
                cap_p = x[ps:pe]
                ts = x.find('<hp:tbl ', pe)
                head_end = x.find('<hp:tr>', ts)
                ok = ('<hp:tbl ' not in cap_p and x[pe:pe + 6] == '<hp:p ' and 0 <= ts - pe < 400
                      and '<hp:caption' not in x[ts:head_end] and 'treatAsChar="1"' in x[ts:head_end])
                if not ok:
                    pos = pe
                    continue
                head = x[ts:head_end]
                width = re.search(r'<hp:sz width="(\d+)"', head).group(1)
                im = head.find('<hp:inMargin ')
                cap = (f'<hp:caption side="TOP" fullSz="0" width="8504" gap="{gap}" lastWidth="{width}">'
                       f'{sub}{cap_p}</hp:subList></hp:caption>')
                x = x[:ps] + x[pe:ts] + head[:im] + cap + head[im:] + x[head_end:]
                moved.append(re.sub(r'<[^>]+>', '', cap_p)[:30])
                pos = ps
            self.secs[k] = x
        return moved

    # ---------- 저장 ----------
    def save(self, out, allow_text_change=False):
        if not allow_text_change:
            assert self.plain() == self._text0, '글 내용이 바뀌었음 (서식만 고치려던 것이면 버그)'
        with zipfile.ZipFile(out, 'w') as zo:
            for it in self.z.infolist():
                n = it.filename
                if n in self.secs:
                    data = self.secs[n].encode('utf-8')
                elif n == 'Contents/header.xml':
                    data = self.header.encode('utf-8')
                else:
                    data = self.bins.get(n, None) or self.z.read(n)
                zo.writestr(it, data, compress_type=it.compress_type)   # 원래 순서·압축 방식 유지
        try:
            import hwpx
            rep = hwpx.validate_editor_open_safety(out)
            assert rep.ok, rep.summary
        except ImportError:
            print('python-hwpx 가 없어 열기 검사는 건너뜀', file=sys.stderr)


# ---------- header.xml 블록 편집 함수 (Hwpx.clone 에 넘긴다) ----------
def edit_align(value):
    """문단 정렬: JUSTIFY(양쪽) / LEFT / CENTER / RIGHT.
    양쪽 맞춤 + 긴 영문 이름이면 낱말 사이가 크게 벌어진다 → LEFT 로 바꾸는 것이 가장 확실했다."""
    return lambda b: re.sub(r'horizontal="\w+"', f'horizontal="{value}"', b, count=1)


def edit_intent_zero(b):
    """내어쓰기·들여쓰기를 0 으로. paraPr 에는 hp:switch 로 같은 값이 두 벌(hp:case / hp:default,
    단위가 달라 값이 2배) 들어 있어서 둘 다 바꿔야 한글에 반영된다."""
    return re.sub(r'<hc:intent value="-?\d+"', '<hc:intent value="0"', b)


def edit_keep_with_next(b):
    return b.replace('keepWithNext="0"', 'keepWithNext="1"')


def edit_spacing(delta):
    """자간을 delta % 만큼 (한글의 Shift+Alt+N 한 번 = -1 %, Shift+Alt+W = +1 %)."""
    def f(b):
        sp = re.search(r'<hh:spacing [^>]*/>', b).group(0)
        new = re.sub(r'="(-?\d+)"', lambda m: f'="{int(m.group(1)) + delta}"', sp)
        return b.replace(sp, new, 1)
    return f


def new_object_id(xml):
    """표·그림을 복제할 때 쓸 겹치지 않는 id."""
    while True:
        i = str(random.randint(10 ** 8, 2 * 10 ** 9))
        if f'id="{i}"' not in xml:
            return i


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['stats', 'relayout', 'replace', 'caption'])
    ap.add_argument('src')
    ap.add_argument('out', nargs='?')
    ap.add_argument('--old')
    ap.add_argument('--new')
    ap.add_argument('--count', type=int, default=1)
    ap.add_argument('--pattern', default=r'&lt;표 [\d-]+&gt;')
    a = ap.parse_args()
    doc = Hwpx(a.src)
    allx = ''.join(doc.secs.values())
    if a.cmd == 'stats':
        print('문단', allx.count('<hp:p '), '표', allx.count('<hp:tbl '), '그림', allx.count('<hp:pic '),
              '캡션', allx.count('<hp:caption '), '줄 배치 캐시', allx.count('<hp:linesegarray'))
        print('문단 모양', re.search(r'<hh:paraProperties itemCnt="(\d+)"', doc.header).group(1),
              '글자 모양', re.search(r'<hh:charProperties itemCnt="(\d+)"', doc.header).group(1))
        return
    assert a.out, '결과 파일 경로가 필요함'
    if a.cmd == 'relayout':
        print('지운 줄 배치 캐시', doc.strip_lineseg())
        doc.save(a.out)
    elif a.cmd == 'replace':
        print('바꾼 곳', doc.replace_text(a.old, a.new, a.count))
        doc.strip_lineseg()
        doc.save(a.out, allow_text_change=True)
    elif a.cmd == 'caption':
        moved = doc.table_title_to_caption(a.pattern)
        print('캡션으로 옮긴 제목', len(moved))
        doc.strip_lineseg()
        doc.save(a.out)
    print('저장', a.out)


if __name__ == '__main__':
    main()
