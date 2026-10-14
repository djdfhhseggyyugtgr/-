#!/usr/bin/env python3
"""Comparison prototypes for the heroine style decision (proportion and face resolution).

Builds four GeckoLib .bbmodel variants of the same placeholder heroine through the headless
Blockbench MCP server, renders them, and composes one comparison sheet.

  A  5.5 heads, no mixels         (face 11 texels wide at 32 px/block)
  B  4.3 heads, bigger head       (face 14 texels)
  C  5.5 heads, mixel eyes only   (eye cubes at 4 texels per unit)
  D  5.5 heads built at 4/3 size  (face 15 texels; meant to render at 0.75 scale in game)

The design is a throwaway placeholder for comparing styles, not an approved character.

usage: VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json \
       python3 tools/art/proto_heroine.py <node24-path> [out_dir]
"""
import base64
import io
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bbmcp import Mcp  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PX_PER_UNIT = 2  # 32 px per block

PAL = {
    'skin': dict(base=(244, 214, 196), s1=(229, 178, 160), s2=(203, 140, 135), hi=(252, 232, 218)),
    'hair': dict(base=(38, 44, 74), s1=(28, 31, 56), s2=(19, 20, 38), hi=(84, 98, 148)),
    'coat': dict(base=(52, 54, 64), s1=(40, 41, 50), s2=(28, 28, 36), hi=(80, 82, 94)),
    'trim': dict(base=(206, 168, 82), s1=(170, 128, 58), s2=(130, 92, 44), hi=(240, 214, 140)),
    'shirt': dict(base=(232, 229, 222), s1=(204, 200, 196), s2=(170, 168, 172), hi=(248, 247, 242)),
    'tights': dict(base=(34, 32, 44), s1=(26, 24, 34), s2=(18, 17, 24), hi=(58, 56, 72)),
    'boots': dict(base=(70, 52, 44), s1=(54, 40, 34), s2=(38, 28, 24), hi=(102, 78, 64)),
    'skirt': dict(base=(44, 46, 60), s1=(34, 35, 48), s2=(24, 24, 34), hi=(66, 70, 90)),
}
EYE = dict(lash=(26, 22, 40), hi=(110, 214, 188), mid=(52, 170, 146), lo=(28, 104, 98),
           pupil=(16, 48, 52), white=(236, 240, 246), glint=(255, 255, 255))
BROW, MOUTH, BLUSH = (40, 40, 66), (176, 92, 98), (242, 168, 164)

VARIANTS = {
    'A': dict(H=30, heads=5.5, legs=0.47, scale=1.0, eyes='texel', label='A  5.5등신 · 믹셀 금지', note='얼굴 11텍셀'),
    'B': dict(H=31, heads=4.3, legs=0.43, scale=1.0, eyes='texel', label='B  4.3등신 · 믹셀 금지 (권장)', note='얼굴 14텍셀'),
    'C': dict(H=30, heads=5.5, legs=0.47, scale=1.0, eyes='mixel', label='C  5.5등신 · 눈만 믹셀', note='눈 4텍셀/유닛'),
    'D': dict(H=30, heads=5.5, legs=0.47, scale=4 / 3, eyes='texel', label='D  5.5등신 · 0.75배 렌더', note='얼굴 15텍셀'),
}


def snap(v):
    return round(v * 2) / 2


def build_parts(v):
    """Return (groups, parts, meta) in model units for one variant."""
    s = v['scale']
    H = v['H']
    h = snap(H / v['heads'] * s)
    L = snap(H * v['legs'] * s)
    nk = snap(1 * s)
    T = snap(H * s) - h - nk  # top of the torso
    sc = lambda x: snap(x * s)  # noqa: E731
    parts, groups = [], []

    def g(name, origin, parent=None):
        groups.append(dict(name=name, origin=origin, parent=parent))

    def c(name, frm, to, mat, parent, rot=None, origin=None, style=None):
        parts.append(dict(name=name, frm=frm, to=to, mat=mat, parent=parent, rot=rot, origin=origin, style=style))

    g('root', [0, 0, 0])
    g('leg_l', [sc(1.5), L, 0], 'root')
    g('leg_r', [-sc(1.5), L, 0], 'root')
    g('body', [0, L, 0], 'root')
    g('skirt', [0, L + sc(0.5), 0], 'body')
    g('arm_l', [sc(4.25), T - sc(0.5), 0], 'body')
    g('arm_r', [-sc(4.25), T - sc(0.5), 0], 'body')
    g('head', [0, T + nk, 0], 'body')
    g('hair', [0, T + nk + h, 0], 'head')

    # legs
    for side, sign in (('l', 1), ('r', -1)):
        x0, x1 = sorted((sign * sc(0.25), sign * sc(2.75)))
        bx0, bx1 = sorted((sign * sc(0.05), sign * sc(2.95)))
        c(f'boot_{side}', [bx0, 0, -sc(2)], [bx1, sc(2.5), sc(1.5)], 'boots', f'leg_{side}', style='boot')
        c(f'shin_{side}', [x0, sc(2.5), -sc(1.25)], [x1, snap(L / 2), sc(1.25)], 'tights', f'leg_{side}')
        c(f'thigh_{side}', [x0, snap(L / 2), -sc(1.25)], [x1, L, sc(1.25)], 'tights', f'leg_{side}')
    # torso
    c('hips', [-sc(3.25), L - sc(1), -sc(1.75)], [sc(3.25), L + sc(1.5), sc(1.75)], 'skirt', 'body')
    c('waist', [-sc(2.5), L + sc(1.5), -sc(1.5)], [sc(2.5), L + sc(3.5), sc(1.5)], 'coat', 'body', style='jacket')
    c('belt', [-sc(2.75), L + sc(1.25), -sc(1.75)], [sc(2.75), L + sc(2), sc(1.75)], 'trim', 'body')
    c('chest', [-sc(3.25), L + sc(3.5), -sc(1.75)], [sc(3.25), T, sc(1.75)], 'coat', 'body', style='jacket')
    c('chest_front', [-sc(2.25), L + sc(4.5), -sc(2.25)], [sc(2.25), L + sc(6.5), -sc(1.75)], 'coat', 'body', style='jacket')
    c('collar', [-sc(2.25), T - sc(0.5), -sc(2)], [sc(2.25), T + sc(0.5), sc(2)], 'coat', 'body', style='trim_bottom')
    c('neck', [-sc(0.75), T, -sc(0.75)], [sc(0.75), T + nk, sc(0.75)], 'skin', 'body')
    # skirt panels and coat tails
    sk_top, sk_bot = L + sc(0.5), L - sc(4)
    c('skirt_f', [-sc(3.5), sk_bot, -sc(2.25)], [sc(3.5), sk_top, -sc(1.75)], 'skirt', 'skirt',
      rot=[-10, 0, 0], origin=[0, sk_top, -sc(2)], style='pleats')
    c('skirt_b', [-sc(3.5), sk_bot, sc(1.75)], [sc(3.5), sk_top, sc(2.25)], 'skirt', 'skirt',
      rot=[10, 0, 0], origin=[0, sk_top, sc(2)], style='pleats')
    for side, sign in (('l', 1), ('r', -1)):
        x0, x1 = sorted((sign * sc(3.25), sign * sc(3.75)))
        c(f'skirt_{side}', [x0, sk_bot, -sc(2)], [x1, sk_top, sc(2)], 'skirt', 'skirt',
          rot=[0, 0, sign * 10], origin=[sign * sc(3.5), sk_top, 0], style='pleats')
    c('coat_tail', [-sc(3), L - sc(7), sc(2.25)], [sc(3), L + sc(1.5), sc(2.75)], 'coat', 'body',
      rot=[8, 0, 0], origin=[0, L + sc(1.5), sc(2.5)], style='trim_bottom')
    # arms
    for side, sign in (('l', 1), ('r', -1)):
        x0, x1 = sorted((sign * sc(3.25), sign * sc(5.25)))
        c(f'upper_arm_{side}', [x0, T - sc(5.5), -sc(1)], [x1, T, sc(1)], 'coat', f'arm_{side}')
        c(f'cuff_{side}', [x0, T - sc(6.25), -sc(1.25)], [x1, T - sc(5.5), sc(1.25)], 'trim', f'arm_{side}')
        c(f'forearm_{side}', [x0, T - sc(10), -sc(1)], [x1, T - sc(6.25), sc(1)], 'shirt', f'arm_{side}')
        c(f'hand_{side}', [x0, T - sc(11.5), -sc(1)], [x1, T - sc(10), sc(1)], 'skin', f'arm_{side}')
    # head and face
    hy = T + nk
    hh = h / 2
    c('head', [-hh, hy, -hh], [hh, hy + h, hh], 'skin', 'head', style='face')
    top = hy + h
    o = sc(0.5)
    # hair shell
    c('hair_top', [-hh - o, top, -hh - o], [hh + o, top + sc(0.75), hh + o], 'hair', 'hair', style='hair')
    c('hair_back', [-hh - o, top - snap(h * 1.25), hh], [hh + o, top, hh + 2 * o], 'hair', 'hair', style='hair')
    for side, sign in (('l', 1), ('r', -1)):
        x0, x1 = sorted((sign * hh, sign * (hh + o + sc(0.25))))
        c(f'hair_side_{side}', [x0, top - snap(h * 0.9), -hh + o], [x1, top, hh + o], 'hair', 'hair', style='hair')
        lx0, lx1 = sorted((sign * (hh - sc(0.5)), sign * (hh + sc(0.5))))
        c(f'side_lock_{side}', [lx0, top - snap(h * 1.15), -hh - sc(0.75)], [lx1, top - snap(h * 0.2), -hh + sc(0.25)],
          'hair', 'hair', style='hair')
    # bangs: five overlapping strands in front of the forehead
    lengths = [0.34, 0.42, 0.3, 0.44, 0.36]
    n = len(lengths)
    w = h / n
    for i, frac in enumerate(lengths):
        x0 = -hh + i * w - 0.01
        c(f'bang_{i}', [snap(x0), snap(top - h * frac), -hh - sc(0.75)], [snap(x0 + w + 0.02), top + sc(0.25), -hh - sc(0.25)],
          'hair', 'hair', rot=[-7.5, 0, (i - 2) * 4], origin=[snap(x0 + w / 2), top, -hh - sc(0.5)], style='hair')
    # ponytail
    c('hair_tie', [-sc(1), top - snap(h * 0.3), hh + 2 * o], [sc(1), top - snap(h * 0.3) + sc(1.5), hh + 2 * o + sc(1)], 'trim', 'hair')
    y = top - snap(h * 0.3)
    for i, (wd, ln, ang) in enumerate(((2.5, 0.75, 18), (2.0, 0.75, 10), (1.5, 0.6, 4))):
        wd, ln = sc(wd), snap(h * ln)
        z0 = hh + 2 * o + sc(0.5)
        c(f'tail_{i}', [-wd / 2, y - ln, z0], [wd / 2, y + sc(0.5), z0 + sc(1.5)], 'hair', 'hair',
          rot=[ang, 0, 0], origin=[0, y, z0 + sc(0.75)], style='hair')
        y = y - ln + snap(math.sin(math.radians(ang)) * 0.5)
    c('ahoge', [-sc(0.25), top + sc(0.5), -sc(1)], [sc(0.25), top + sc(2.5), -sc(0.5)], 'hair', 'hair',
      rot=[-25, 0, 15], origin=[0, top + sc(0.5), -sc(0.75)], style='hair')

    meta = dict(h=h, hy=hy, top=top, L=L, T=T, face_px=int(h * PX_PER_UNIT))
    if v['eyes'] == 'mixel':
        ew, eh = 1.5, 2.0
        ey = hy + h - h * 0.42 - eh  # eye top at 42% down the face
        for side, sign in (('l', 1), ('r', -1)):
            cx = sign * h * 0.25
            c(f'eye_{side}', [cx - ew / 2, ey, -hh - 0.06], [cx + ew / 2, ey + eh, -hh - 0.01], 'skin', 'head', style='mixel_eye')
    return groups, parts, meta


class Atlas:
    """Shelf packer for per-face UV rectangles."""

    def __init__(self, size):
        self.size, self.x, self.y, self.row = size, 0, 0, 0

    def alloc(self, w, h):
        w, h = max(1, w), max(1, h)
        if self.x + w > self.size:
            self.x, self.y, self.row = 0, self.y + self.row, 0
        if self.y + h > self.size:
            raise OverflowError
        r = (self.x, self.y, w, h)
        self.x += w
        self.row = max(self.row, h)
        return r


FACE_DIMS = {
    'north': (0, 1), 'south': (0, 1), 'east': (2, 1), 'west': (2, 1), 'up': (0, 2), 'down': (0, 2),
}


def face_rects(parts, size):
    atlas = Atlas(size)
    for p in parts:
        dims = [abs(b - a) for a, b in zip(p['frm'], p['to'])]
        p['uv'] = {}
        for face, (ai, bi) in FACE_DIMS.items():
            ppu = 4 if p['style'] == 'mixel_eye' else PX_PER_UNIT
            if p['style'] == 'mixel_eye' and face != 'north':
                continue
            w, h = math.ceil(dims[ai] * ppu - 1e-6), math.ceil(dims[bi] * ppu - 1e-6)
            p['uv'][face] = atlas.alloc(w, h)


def paint(img, parts, meta, variant):
    px = img.load()
    for p in parts:
        pal = PAL[p['mat']]
        for face, (x0, y0, w, h) in p['uv'].items():
            for yy in range(h):
                for xx in range(w):
                    col = pal['base']
                    if face == 'up':
                        col = pal['hi'] if p['mat'] in ('hair', 'trim') else pal['base']
                    elif face == 'down':
                        col = pal['s2']
                    else:
                        if h >= 4 and yy >= h - max(1, h // 4):
                            col = pal['s1']
                        if h >= 6 and yy == h - 1:
                            col = pal['s2']
                        if p['style'] == 'hair' and xx % 3 == 2 and yy > 0:
                            col = pal['s1']
                        if p['style'] == 'hair' and yy == 1 and h > 4:
                            col = pal['hi']
                        if p['style'] == 'pleats' and xx % 4 == 3:
                            col = pal['s1']
                        if p['style'] == 'trim_bottom' and yy >= h - 2:
                            col = PAL['trim']['base'] if yy == h - 2 else PAL['trim']['s1']
                        if p['style'] == 'boot' and yy < 2:
                            col = PAL['trim']['s1']
                    px[x0 + xx, y0 + yy] = col + (255,)
            if p['style'] == 'jacket' and face == 'north':
                paint_jacket(px, x0, y0, w, h)
            if p['style'] == 'face' and face == 'north':
                paint_face(px, x0, y0, w, variant)
            if p['style'] == 'mixel_eye':
                paint_mixel_eye(px, x0, y0, w, h)


def paint_jacket(px, x0, y0, w, h):
    mid = w // 2
    open_w = max(2, w // 3)
    for yy in range(h):
        half = max(1, open_w // 2 - yy // 3)
        for xx in range(mid - half, mid + half):
            px[x0 + xx, y0 + yy] = PAL['shirt']['base'] + (255,)
        for xx in (mid - half - 1, mid + half):
            if 0 <= xx < w:
                px[x0 + xx, y0 + yy] = PAL['trim']['base'] + (255,)


def paint_face(px, x0, y0, f, variant):
    skin = PAL['skin']
    for yy in range(max(1, round(f * 0.3))):
        for xx in range(f):
            px[x0 + xx, y0 + yy] = skin['s1'] + (255,)  # shadow under the bangs
    ew = 2 if f < 13 else 3
    eh = ew + 1
    ey = y0 + round(f * 0.42)
    margin = round(f * 0.18)
    eyes = (x0 + margin, x0 + f - margin - ew)
    mixel = variant['eyes'] == 'mixel'
    for ex in eyes:
        for xx in range(ew):  # brow
            px[ex + xx, ey - 2] = BROW + (255,)
        if mixel:
            continue
        for xx in range(-1 if ex == eyes[0] else 0, ew + (1 if ex == eyes[1] else 0)):
            px[ex + xx, ey] = EYE['lash'] + (255,)
        for yy in range(1, eh):
            for xx in range(ew):
                col = EYE['hi'] if yy == 1 else EYE['lo'] if yy == eh - 1 else EYE['mid']
                px[ex + xx, ey + yy] = col + (255,)
        if ew == 3:
            px[ex + 1, ey + 2] = EYE['pupil'] + (255,)
        px[ex, ey + 1] = EYE['glint'] + (255,)
        if f >= 14:
            bx = ex - 1 if ex == eyes[0] else ex + ew
            px[bx, ey + eh] = BLUSH + (255,)
    my = y0 + round(f * 0.78)
    mw = 1 if f < 13 else 2
    for xx in range(mw):
        px[x0 + f // 2 - mw // 2 + xx, my] = MOUTH + (255,)


def paint_mixel_eye(px, x0, y0, w, h):
    """6x8 texel eye at 4 texels per unit: lashes, iris gradient, pupil, two glints."""
    for yy in range(h):
        for xx in range(w):
            if yy < 2:
                col = EYE['lash']
            elif yy == h - 1:
                col = EYE['lo']
            elif xx in (0, w - 1):
                col = EYE['white']
            elif yy < 4:
                col = EYE['hi']
            elif yy < 6:
                col = EYE['mid']
            else:
                col = EYE['lo']
            px[x0 + xx, y0 + yy] = col + (255,)
    for yy in (4, 5):
        for xx in (2, 3):
            px[x0 + xx, y0 + yy] = EYE['pupil'] + (255,)
    px[x0 + 1, y0 + 2] = EYE['glint'] + (255,)
    px[x0 + 2, y0 + 2] = EYE['glint'] + (255,)
    px[x0 + 4, y0 + 6] = EYE['glint'] + (255,)


def to_data_url(img):
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def build(m, key, v, out_rel):
    groups, parts, meta = build_parts(v)
    for size in (128, 256, 512):
        try:
            face_rects(parts, size)
            break
        except OverflowError:
            continue
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    paint(img, parts, meta, v)
    m.call('bbmodel_create', {'file': out_rel, 'format': 'geckolib_model', 'name': f'proto_heroine_{key}', 'box_uv': False,
                              'resolution': {'width': size, 'height': size}, 'overwrite': True})
    rev = m.call('bbmodel_info', {'file': out_rel})['revision']
    ops = [{'op': 'add_texture', 'name': f'proto_heroine_{key}', 'source': to_data_url(img), 'width': size, 'height': size}]
    for gr in groups:
        ops.append({'op': 'add_group', 'name': gr['name'], 'origin': gr['origin'], 'parent': gr['parent']})
    for p in parts:
        faces = {f: {'uv': [x, y, x + w, y + h], 'texture': 0} for f, (x, y, w, h) in p['uv'].items()}
        for f in FACE_DIMS:
            faces.setdefault(f, {'texture': None})
        op = {'op': 'add_cube', 'name': p['name'], 'from': p['frm'], 'to': p['to'], 'parent': p['parent'], 'faces': faces}
        if p['rot']:
            op['rotation'] = p['rot']
            op['origin'] = p['origin']
        ops.append(op)
    res = m.call('bbmodel_edit', {'file': out_rel, 'expected_revision': rev, 'operations': ops})
    val = m.call('bbmodel_validate', {'file': out_rel})
    return meta, len(parts), size, val, res.get('web_app', {})


def render(m, rel, key):
    shots = {}
    render_dir = os.path.join(REPO, 'models', 'proto', 'render')
    os.makedirs(render_dir, exist_ok=True)
    for view, persp in (('front', False), ('three-quarter', True), ('back', False)):
        out = os.path.join(render_dir, f'{key}_{view}.png')
        m.call('bbmodel_render', {'file': rel, 'view': view, 'width': 900, 'height': 900, 'orthographic': not persp,
                                  'lighting': 'studio' if persp else 'flat', 'transparent': True,
                                  'output': os.path.relpath(out, os.path.join(REPO, 'models')), 'overwrite': True})
        shots[view] = out
    return shots


def face_crop(path, meta):
    im = Image.open(path).convert('RGBA')
    x0, y0, x1, y1 = im.getbbox()
    model_top = meta['top'] + 2.5 * (meta['h'] / 5.5)  # ahoge sits above the hair
    frac = (model_top - (meta['hy'] - 1)) / model_top
    hy1 = y0 + int((y1 - y0) * frac)
    cx = (x0 + x1) // 2
    side = hy1 - y0
    return im.crop((cx - side // 2, y0, cx + side // 2, hy1))


def compose(results, out_path):
    font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
    font = ImageFont.truetype(font_path, 30) if os.path.exists(font_path) else ImageFont.load_default()
    small = ImageFont.truetype(font_path, 22) if os.path.exists(font_path) else ImageFont.load_default()
    col_w, body_h, face_h, pad, head = 420, 620, 420, 24, 110
    W = len(results) * (col_w + pad) + pad
    Hh = head + body_h * 2 + face_h + pad * 5 + 60
    sheet = Image.new('RGB', (W, Hh), (30, 31, 36))
    d = ImageDraw.Draw(sheet)
    d.text((pad, Hh - 50), '비교용 임시 시안 (디자인 미확정) · 32px/블록 · 클라우드 CPU 렌더', font=small, fill=(170, 170, 180))
    for i, (key, r) in enumerate(results.items()):
        x = pad + i * (col_w + pad)
        d.text((x, 20), VARIANTS[key]['label'], font=font, fill=(235, 235, 240))
        d.text((x, 62), f"{VARIANTS[key]['note']} · 큐브 {r['cubes']}개", font=small, fill=(180, 180, 190))
        y = head
        for view in ('front', 'three-quarter'):
            im = Image.open(r['shots'][view]).convert('RGBA')
            im = im.crop(im.getbbox())
            im.thumbnail((col_w, body_h), Image.NEAREST)
            sheet.paste(im, (x + (col_w - im.width) // 2, y + (body_h - im.height) // 2), im)
            y += body_h + pad
        fc = r['face']
        fc = fc.resize((col_w, int(fc.height * col_w / fc.width)), Image.NEAREST)
        fc = fc.crop((0, 0, col_w, min(face_h, fc.height)))
        sheet.paste(fc, (x, y), fc)
    sheet.save(out_path)


def main():
    node24 = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, 'docs', 'design', 'proto')
    os.makedirs(out_dir, exist_ok=True)
    m = Mcp(['node', os.path.join(REPO, 'tools', 'mcp', 'bbmodel-headless.mjs'), '--node', node24])
    results = {}
    try:
        for key, v in VARIANTS.items():
            rel = f'proto/heroine_{key}.bbmodel'
            meta, n, size, val, web = build(m, key, v, rel)
            summary = val.get('summary', val) if isinstance(val, dict) else val
            print(f'{key}: cubes={n} atlas={size}px face={meta["face_px"]}px validate={summary}')
            shots = render(m, rel, key)
            results[key] = dict(cubes=n, shots=shots, face=face_crop(shots['front'], meta), web=web)
        compose(results, os.path.join(out_dir, 'heroine_style_compare.png'))
        print('sheet:', os.path.join(out_dir, 'heroine_style_compare.png'))
    finally:
        m.close()


if __name__ == '__main__':
    main()
