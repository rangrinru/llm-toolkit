"""표 열 너비를 다시 나눠, 칸 안에서 한두 글자만 다음 줄로 넘어가거나 긴 영문 이름이 잘리는 것을 고친다.

방법
- 보기 싫은 끝줄이 있는 칸의 열을 150 HWPUNIT 씩 넓히고, 그만큼 다른 열에서 50 씩 가져온다.
  가져오는 열은 원래 폭의 60 % 아래로 줄이지 않고, 그 열의 다른 칸 줄 수가 늘지 않을 때만 가져온다.
- 넓혀서 안 되면 반대로 그 열을 좁혀(최대 25 %) 끝줄에 글자가 더 모이게 해 본다.
- 한 번 고친 칸은 이후 다른 칸을 고치다가 다시 망가지지 않게 지킨다.
- 표 전체 폭은 그대로. 병합 칸(colSpan)이 있어도 열마다 폭을 정할 수 있는 표만 다룬다.

사용법
    python rebalance_columns.py 문서.hwpx 결과.hwpx --start "요약문" --end "(3)세부정량적" [--dry-run]
"""
import argparse
import io
import re
import sys
import zipfile

from linebreak_sim import Doc
from tidy_paragraphs import in_range


def tables_in_range(d, start, end, skip_start=None, skip_end=None):
    """범위 안의 표 중 다른 표를 품지 않은 것(본문을 감싸는 큰 틀 표는 제외)."""
    out = []
    for p in in_range(d, start, end, skip_start, skip_end):
        for tbl in p.iter(d.HP + 'tbl'):
            if tbl.find('.//hp:tbl', d.ns) is None and tbl not in out:
                out.append(tbl)
    return out


def title(d, tbl):
    cap = tbl.find('hp:caption', d.ns)
    return ''.join(t.text or '' for t in cap.iter(d.HP + 't'))[:24] if cap is not None else '(제목 없음)'


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--start', required=True); ap.add_argument('--end', required=True)
    ap.add_argument('--skip-start'); ap.add_argument('--skip-end')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    d = Doc(a.src)
    assert d.serialize() == d.raw, 'lxml 로 다시 쓰면 원본과 달라짐 → 이 문서에는 쓰지 말 것'

    def state(p, cw, margin, f):
        n = len(d.lines(p, (cw - margin) * f))
        return n, d.bad_last_line(p, (cw - margin) * f)

    def good(p, cw, margin):
        return not any(state(p, cw, margin, f)[1] for f in (0.98, 1.0, 1.02))

    def not_worse(p, cw, margin, n0, b0):
        for f in (0.98, 1.0):
            n1, b1 = state(p, cw, margin, f)
            if n1 > n0 or (b1 and not b0):
                return False
        return True

    skipped, changed = [], []
    for tbl in tables_in_range(d, a.start, a.end, a.skip_start, a.skip_end):
        cells = []
        for tc in tbl.iter(d.HP + 'tc'):
            addr, span, sz = (tc.find(f'hp:{k}', d.ns) for k in ('cellAddr', 'cellSpan', 'cellSz'))
            ps = [p for p in tc.iter(d.HP + 'p') if d.text(p).strip()]
            w0 = int(sz.get('width'))
            cells.append(dict(sz=sz, c0=int(addr.get('colAddr')), n=int(span.get('colSpan')), ps=ps, w0=w0,
                              margin=w0 - d.cell_width(ps[0]) if ps else 0))
        ncol = int(tbl.get('colCnt'))
        w = [None] * ncol
        for c in cells:
            if c['n'] == 1:
                w[c['c0']] = c['w0']
        cw = lambda c, ww: sum(ww[c['c0']:c['c0'] + c['n']])
        if None in w or any(abs(cw(c, w) - c['w0']) > 3 for c in cells):
            skipped.append(title(d, tbl))
            continue
        base = {id(c): [state(p, c['w0'], c['margin'], 1.0) for p in c['ps']] for c in cells}

        def ok_all(ww, fixing):
            for c in cells:
                for p, (n0, b0) in zip(c['ps'], base[id(c)]):
                    if c is fixing:
                        if not good(p, cw(c, ww), c['margin']):
                            return False
                    elif not not_worse(p, cw(c, ww), c['margin'], n0, b0):
                        return False
            return True

        def donors_ok(ww, j):
            return all(not_worse(p, cw(x, ww), x['margin'], n0, b0)
                       for x in cells if x['c0'] <= j < x['c0'] + x['n']
                       for p, (n0, b0) in zip(x['ps'], base[id(x)]))

        W, log = list(w), []
        for c in [c for c in cells if any(b for _, b in base[id(c)])]:
            if all(good(p, cw(c, W), c['margin']) for p in c['ps']):
                continue
            cols = list(range(c['c0'], c['c0'] + c['n']))
            tgt, others = cols[-1], [j for j in range(ncol) if j not in cols]
            done = False
            for dw in range(150, int(cw(c, W) * 0.6), 150):          # 넓히기
                trial, need, rot = list(W), dw, list(others)
                trial[tgt] += dw
                while need > 0:
                    for j in rot:
                        t2 = list(trial)
                        t2[j] -= min(50, need)
                        if t2[j] >= max(1500, w[j] * 0.6) and donors_ok(t2, j):
                            trial, need = t2, need - min(50, need)
                            rot = rot[rot.index(j):] + rot[:rot.index(j)]
                            break
                    else:
                        break
                if need == 0 and ok_all(trial, c):
                    W, done = trial, True
                    break
            if not done:                                             # 좁히기
                for dw in range(150, int(W[tgt] * 0.25), 150):
                    trial = list(W)
                    trial[tgt] -= dw
                    for k, j in enumerate(others):
                        trial[j] += dw // len(others) + (1 if k < dw % len(others) else 0)
                    if ok_all(trial, c):
                        W, done = trial, True
                        break
            if done:
                base[id(c)] = [(state(p, cw(c, W), c['margin'], 1.0)[0], False) for p in c['ps']]
            log.append(('고침' if done else '못 고침', d.text(c['ps'][0])[:26]))
        if W != w:
            for c in cells:
                c['sz'].set('width', str(cw(c, W)))
        if log:
            changed.append((title(d, tbl), [(i, x, y) for i, (x, y) in enumerate(zip(w, W)) if x != y], log))

    for nm, ch, log in changed:
        print(nm, '| 열(번호, 전, 후)', ch)
        for s, t in log:
            print('    ', s, '|', t)
    print('열 구조를 정할 수 없어 건너뛴 표:', skipped)
    if a.dry_run:
        return
    new = d.serialize()
    assert re.sub(rb'<[^>]+>', b'', new) == re.sub(rb'<[^>]+>', b'', d.raw), '글 내용이 바뀜'
    with zipfile.ZipFile(a.out, 'w') as zo:
        for it in d.z.infolist():
            zo.writestr(it, new if it.filename == d.section else d.z.read(it.filename), compress_type=it.compress_type)
    try:
        import hwpx
        rep = hwpx.validate_editor_open_safety(a.out)
        assert rep.ok, rep.summary
    except ImportError:
        pass
    print('저장', a.out)


if __name__ == '__main__':
    main()
