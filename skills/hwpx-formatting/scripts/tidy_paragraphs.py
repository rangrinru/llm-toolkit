"""표 칸 안 문단의 서식을 일괄 정리한다.

1. 양쪽 맞춤(JUSTIFY) → 왼쪽 맞춤(LEFT): 긴 영문 이름 때문에 낱말 사이가 벌어지는 것을 없앤다.
2. 글머리표(◦ - ※ ① 1) 등)로 시작하지 않는 문단의 내어쓰기 제거: 둘째 줄부터 왼쪽이 비는 것을 없앤다.
3. 끝줄에 한두 글자만 남는 문단은 자간을 -1 ~ -7 % 줄여 윗줄로 올린다(Shift+Alt+N 과 같음).

문단 모양·글자 모양은 원본을 고치지 않고 복제본을 만들어 바꾼다(같은 모양을 쓰는 다른 문단 보호).
줄 나뉨은 linebreak_sim 으로 예측한 것이므로 한글에서 반드시 눈으로 확인한다.

사용법
    python tidy_paragraphs.py 문서.hwpx 결과.hwpx --start "요약문" --end "(3)세부정량적" \
        [--skip-start "요약문작성요령" --skip-end "각항목에서요구하는"] [--dry-run]
    (--start 등은 띄어쓰기를 뺀 글로 비교한다)
"""
import argparse
import io
import re
import sys
import zipfile

from linebreak_sim import Doc
from hwpx_patch import edit_spacing

BULLET = re.compile(r'^\s*(◦|○|ㅇ|□|■|▪|·|•|-|–|※|\*|[①-⑳]|\(?\d+\)|\d+\.|[가-하]\.)\s?')


def in_range(d, start, end, skip_start=None, skip_end=None):
    state = 'before'
    for p in d.paragraphs():
        k = d.text(p).replace(' ', '')
        if state == 'before' and start in k:
            state = 'in'
        elif state == 'in' and skip_start and skip_start in k:
            state = 'skip'
        elif state == 'skip' and skip_end in k:
            state = 'in'
        elif state == 'in' and end in k:
            return
        if state == 'in':
            yield p


class Header:
    """d.h(header.xml 문자열)에 모양을 복제해 넣고, 같은 (원본, 편집) 조합은 한 번만 만든다."""

    def __init__(self, d):
        self.d, self.cache = d, {}

    def clone(self, kind, src, key, edit):
        if (kind, src, key) in self.cache:
            return self.cache[(kind, src, key)]
        grp = {'paraPr': 'paraProperties', 'charPr': 'charProperties'}[kind]
        h = self.d.h
        blk = re.search(r'<hh:%s id="%s".*?</hh:%s>' % (kind, src, kind), h, re.S).group(0)
        m = re.search(r'<hh:%s itemCnt="(\d+)"' % grp, h)
        nid = int(m.group(1))
        nb = edit(blk.replace(f'<hh:{kind} id="{src}"', f'<hh:{kind} id="{nid}"', 1))
        end = h.find(f'</hh:{grp}>')
        h = h[:end] + nb + h[end:]
        self.d.h = h.replace(m.group(0), f'<hh:{grp} itemCnt="{nid + 1}"', 1)
        self.cache[(kind, src, key)] = str(nid)
        return str(nid)


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--start', required=True); ap.add_argument('--end', required=True)
    ap.add_argument('--skip-start'); ap.add_argument('--skip-end')
    ap.add_argument('--max-tighten', type=int, default=7, help='자간을 최대 몇 % 까지 줄일지')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    d = Doc(a.src)
    assert d.serialize() == d.raw, 'lxml 로 다시 쓰면 원본과 달라짐 → 이 문서에는 쓰지 말 것'
    hd = Header(d)
    n_left = n_intent = 0
    tightened, failed = {}, []
    for p in list(in_range(d, a.start, a.end, a.skip_start, a.skip_end)):
        t = d.text(p)
        if not t.strip() or p.find('.//hp:tbl', d.ns) is not None or p.find('.//hp:pic', d.ns) is not None:
            continue
        pid = p.get('paraPrIDRef')
        pp = d.para_pr(pid)
        if pp['align'] not in ('JUSTIFY', 'LEFT'):
            continue                                  # 가운데·오른쪽 맞춤 칸은 두고
        to_left, no_intent = pp['align'] == 'JUSTIFY', pp['intent'] < 0 and not BULLET.match(t)
        if to_left or no_intent:
            def edit(b, l=to_left, z=no_intent):
                if l:
                    b = b.replace('horizontal="JUSTIFY"', 'horizontal="LEFT"')
                if z:
                    b = re.sub(r'<hc:intent value="-?\d+"', '<hc:intent value="0"', b)
                return b
            p.set('paraPrIDRef', hd.clone('paraPr', pid, (to_left, no_intent), edit))
            n_left += to_left
            n_intent += no_intent
        if not d.cell_width(p) or not d.bad_last_line(p):
            continue
        n0 = len(d.lines(p))
        for delta in range(-1, -a.max_tighten - 1, -1):
            # ±2 % 너비 오차에서도 괜찮아야 채택(예측 오차 대비)
            w = d.cell_width(p)
            if all(not d.bad_last_line(p, w * f, delta) for f in (0.98, 1.0, 1.02)) and len(d.lines(p, w, delta)) <= n0:
                for r in p.findall('hp:run', d.ns):
                    r.set('charPrIDRef', hd.clone('charPr', r.get('charPrIDRef'), delta, edit_spacing(delta)))
                tightened[delta] = tightened.get(delta, 0) + 1
                break
        else:
            failed.append((t[:30], d.lines(p)[-1][0][-12:]))

    print(f'왼쪽 맞춤으로 {n_left} | 내어쓰기 제거 {n_intent} | 자간 조정 {sum(tightened.values())} {tightened}')
    print(f'자간으로 못 올린 곳 {len(failed)}')
    for f in failed:
        print('   ', f)
    if a.dry_run:
        return
    new = d.serialize()
    assert re.sub(rb'<[^>]+>', b'', new) == re.sub(rb'<[^>]+>', b'', d.raw), '글 내용이 바뀜'
    with zipfile.ZipFile(a.out, 'w') as zo:
        for it in d.z.infolist():
            data = (new if it.filename == d.section else
                    d.h.encode('utf-8') if it.filename == 'Contents/header.xml' else d.z.read(it.filename))
            zo.writestr(it, data, compress_type=it.compress_type)
    try:
        import hwpx
        rep = hwpx.validate_editor_open_safety(a.out)
        assert rep.ok, rep.summary
    except ImportError:
        pass
    print('저장', a.out)


if __name__ == '__main__':
    main()
