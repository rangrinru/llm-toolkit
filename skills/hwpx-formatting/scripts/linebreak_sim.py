"""HWPX 문단의 줄 나뉨을 글꼴 폭으로 예측하는 계산기 (한글 프로그램 없이 쓰는 근사치).

관찰한 한글 동작
- 문단 모양이 '어절 단위(KEEP_WORD)'여도 한글 글자는 실제로 글자 단위로 줄이 나뉘었다.
- 영문·숫자는 낱말 단위로 넘어가고, 한 줄보다 긴 영문 낱말만 중간에서 잘린다.
- ')' 는 줄 머리에 올 수 있었다(금칙 아님). '.' ',' 는 앞 글자에 붙여 계산한다.
- 실제 화면과 대조하면 6곳 중 4곳은 정확, 2곳은 한 글자 차이였다 → 판정에 ±2 % 여유를 둔다.

사용 예
    python linebreak_sim.py 문서.hwpx "찾을 문장 일부"

    from linebreak_sim import Doc
    d = Doc('report.hwpx')
    for p in d.paragraphs():
        if d.cell_width(p):
            for text, width, limit in d.lines(p):
                print(f'{width / limit:5.1%} | {text}')
"""
import re
import zipfile
import functools
from lxml import etree
from PIL import ImageFont

# 문서 글꼴 이름 → (글꼴 파일, ttc 안 번호). 목록에 없는 글꼴은 DEFAULT_FACE 로 대신 잰다.
FONTFILE = {
    '돋움': ('C:/Windows/Fonts/gulim.ttc', 2),
    '돋움체': ('C:/Windows/Fonts/gulim.ttc', 3),
    '굴림': ('C:/Windows/Fonts/gulim.ttc', 0),
    '바탕': ('C:/Windows/Fonts/batang.ttc', 0),
    '맑은 고딕': ('C:/Windows/Fonts/malgun.ttf', 0),
}
DEFAULT_FACE = '맑은 고딕'
EM = 2000
NO_START = set('.,!?%:;·~…°' + chr(34) + chr(39) + chr(0x201d) + chr(0x2019))   # 앞 글자에 붙여 계산
NO_END = set('([{' + chr(0x201c) + chr(0x2018) + '「『〈《')                      # 뒤 글자에 붙여 계산


@functools.lru_cache(None)
def _font(face):
    path, idx = FONTFILE.get(face, FONTFILE[DEFAULT_FACE])
    return ImageFont.truetype(path, EM, index=idx)


@functools.lru_cache(None)
def advance(face, ch):
    """글자 하나의 폭(em 비율)."""
    return _font(face).getlength(ch) / EM


def _is_latin(ch):
    return 0x21 <= ord(ch) <= 0x7e


class Doc:
    def __init__(self, path, section='Contents/section0.xml'):
        self.z = zipfile.ZipFile(path)
        self.h = self.z.read('Contents/header.xml').decode('utf-8')
        self.section = section
        self.raw = self.z.read(section)
        self.root = etree.fromstring(self.raw)
        self.ns = {'hp': self.root.nsmap['hp']}
        self.HP = '{%s}' % self.ns['hp']
        faces = re.search(r'<hh:fontface lang="HANGUL".*?</hh:fontface>', self.h, re.S).group(0)
        self.faces = dict(re.findall(r'<hh:font id="(\d+)" face="([^"]+)"', faces))
        self._cache = {}           # 모양 id → 값 (id 는 한번 만들면 바뀌지 않으므로 캐시해도 안전)
        self.overflow = False      # 마지막 lines() 결과에 줄보다 긴 영문 낱말이 있었는가
        self.brk = []              # 마지막 lines() 결과에서 각 줄이 띄어쓰기에서 끝났는가

    def serialize(self):
        return (b'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
                + etree.tostring(self.root, encoding='UTF-8'))

    def paragraphs(self):
        return self.root.iter(self.HP + 'p')

    def text(self, p):
        return ''.join(t.text or '' for t in p.findall('hp:run/hp:t', self.ns))

    def char_pr(self, cid):
        if ('c', cid) in self._cache:
            return self._cache[('c', cid)]
        b = re.search(r'<hh:charPr id="%s".*?</hh:charPr>' % cid, self.h, re.S).group(0)
        v = dict(size=int(re.search(r'height="(\d+)"', b).group(1)),
                 face=self.faces[re.search(r'fontRef hangul="(\d+)"', b).group(1)],
                 ratio=int(re.search(r'ratio hangul="(\d+)"', b).group(1)),
                 spacing=int(re.search(r'spacing hangul="(-?\d+)"', b).group(1)))
        self._cache[('c', cid)] = v
        return v

    def para_pr(self, pid):
        """문단 모양. hp:switch 의 두 벌 중 앞(hp:case) 값을 쓴다."""
        if ('p', pid) in self._cache:
            return self._cache[('p', pid)]
        b = re.search(r'<hh:paraPr id="%s".*?</hh:paraPr>' % pid, self.h, re.S).group(0)
        v = dict(align=re.search(r'horizontal="(\w+)"', b).group(1),
                 intent=int(re.search(r'<hc:intent value="(-?\d+)"', b).group(1)),
                 left=int(re.search(r'<hc:left value="(-?\d+)"', b).group(1)),
                 right=int(re.search(r'<hc:right value="(-?\d+)"', b).group(1)))
        self._cache[('p', pid)] = v
        return v

    def cell_width(self, p):
        """문단이 들어 있는 표 칸의 글 너비(HWPUNIT). 표 밖 문단이면 None."""
        tc = p.getparent()
        while tc is not None and tc.tag != self.HP + 'tc':
            tc = tc.getparent()
        if tc is None:
            return None
        w = int(tc.find('hp:cellSz', self.ns).get('width'))
        if tc.get('hasMargin') == '1':
            m = tc.find('hp:cellMargin', self.ns)
        else:
            m = tc.getparent().getparent().find('hp:inMargin', self.ns)
        return w - int(m.get('left')) - int(m.get('right'))

    def chars(self, p, spacing_delta=0):
        out = []
        for r in p.findall('hp:run', self.ns):
            c = self.char_pr(r.get('charPrIDRef'))
            for t in r.findall('hp:t', self.ns):
                for ch in (t.text or ''):
                    a = 0.5 if ch == ' ' else advance(c['face'], ch)
                    sp = 1 + (c['spacing'] + spacing_delta) / 100
                    out.append((ch, a * c['ratio'] / 100 * sp * c['size']))
        return out

    def lines(self, p, width=None, spacing_delta=0):
        """[(줄 글, 줄 폭, 그 줄에 쓸 수 있는 폭), ...]"""
        pp = self.para_pr(p.get('paraPrIDRef'))
        width = width or self.cell_width(p)
        base = width - pp['left'] - pp['right']
        w_first, w_rest = base - max(pp['intent'], 0), base - max(-pp['intent'], 0)
        cs = self.chars(p, spacing_delta)
        toks, i = [], 0                               # 공백 / 영문 낱말 / 그 밖의 글자 하나
        while i < len(cs):
            ch = cs[i][0]
            if ch == ' ':
                toks.append(([cs[i]], 'sp'))
                i += 1
            elif _is_latin(ch):
                j = i
                while j < len(cs) and _is_latin(cs[j][0]):
                    j += 1
                toks.append((cs[i:j], 'lat'))
                i = j
            else:
                toks.append(([cs[i]], 'han'))
                i += 1
        merged = []
        for tk, kind in toks:
            glue = merged and kind != 'sp' and merged[-1][1] != 'sp' and (
                tk[0][0] in NO_START or merged[-1][0][-1][0] in NO_END)
            if glue:
                merged[-1] = (merged[-1][0] + tk, merged[-1][1])
            else:
                merged.append((tk, kind))
        lines, cur, lim = [[]], 0.0, w_first
        for tk, kind in merged:
            w = sum(a for _, a in tk)
            if kind != 'sp' and cur + w > lim + 1 and any(c != ' ' for c, _ in lines[-1]):
                lines.append([])
                cur, lim = 0.0, w_rest
            lines[-1] += tk
            cur += w
        res = []
        for k, ln in enumerate(lines):
            body = ''.join(c for c, _ in ln).rstrip(' ')
            res.append((body, sum(a for _, a in ln[:len(body)]), w_first if k == 0 else w_rest))
        self.overflow = any(wd > lm + 1 for _, wd, lm in res)
        self.brk = [''.join(c for c, _ in ln).endswith(' ') for ln in lines]
        return res

    def bad_last_line(self, p, width=None, spacing_delta=0):
        """보기 싫은 끝줄인가.
        - 줄보다 긴 영문 낱말이 중간에서 잘림
        - 끝줄이 4글자 이하(또는 줄 폭의 12 % 미만)인데 낱말 중간에서 끊김
        - 왼쪽·양쪽 맞춤 문단은 낱말 단위로 넘어간 짧은 끝줄도 포함
          (가운데 맞춤 칸의 '85% / 내외' 같은 낱말 단위 줄바꿈은 자연스러우므로 제외)"""
        ls = self.lines(p, width, spacing_delta)
        if self.overflow:
            return True
        if len(ls) < 2:
            return False
        last = ls[-1][0].strip()
        short = len(last) <= 4 or ls[-1][1] / ls[-1][2] < 0.12
        loose = self.para_pr(p.get('paraPrIDRef'))['align'] in ('LEFT', 'JUSTIFY')
        return bool(short and last and last[0] not in '(-–[' and (not self.brk[-2] or loose))


if __name__ == '__main__':
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if len(sys.argv) < 3:
        sys.exit('사용법: python linebreak_sim.py 문서.hwpx "찾을 문장 일부"')
    d = Doc(sys.argv[1])
    for p in d.paragraphs():
        if sys.argv[2] in d.text(p) and p.find('.//hp:tbl', d.ns) is None and d.cell_width(p):
            for body, wd, lim in d.lines(p):
                print(f'{wd / lim:6.1%} | {body}')
            print('보기 싫은 끝줄' if d.bad_last_line(p) else '괜찮음')
            break
    else:
        print('표 칸 안에서 그 문장을 찾지 못함')
