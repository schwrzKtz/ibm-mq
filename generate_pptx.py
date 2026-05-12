from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# --- Color palette ---
IBM_BLUE    = RGBColor(0x05, 0x2F, 0xAA)   # IBM Blue (deep)
ACCENT_BLUE = RGBColor(0x00, 0x62, 0xFF)   # IBM Blue (light)
BG_LIGHT    = RGBColor(0xF4, 0xF7, 0xFF)   # Slide background
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT   = RGBColor(0x16, 0x1C, 0x2D)
GRAY        = RGBColor(0x69, 0x72, 0x89)
LIGHT_GRAY  = RGBColor(0xE8, 0xEC, 0xF5)
GREEN       = RGBColor(0x24, 0xA1, 0x48)
AMBER       = RGBColor(0xF1, 0xC2, 0x1B)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]  # completely blank

# ── Helpers ───────────────────────────────────────────────────────────────────

def add_rect(slide, l, t, w, h, fill_rgb=None, line_rgb=None, line_width_pt=0):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_rgb
    else:
        shape.fill.background()
    if line_rgb and line_width_pt:
        from pptx.util import Pt as _Pt
        shape.line.color.rgb = line_rgb
        shape.line.width = _Pt(line_width_pt)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, l, t, w, h,
             font_size=18, bold=False, color=DARK_TEXT,
             align=PP_ALIGN.LEFT, italic=False, wrap=True):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tb.word_wrap = wrap
    tf = tb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return tb


def slide_bg(slide, color=BG_LIGHT):
    add_rect(slide, 0, 0, 13.33, 7.5, fill_rgb=color)


def header_bar(slide, title, subtitle=None):
    # Blue bar at top
    add_rect(slide, 0, 0, 13.33, 1.35, fill_rgb=IBM_BLUE)
    add_text(slide, title, 0.5, 0.18, 11, 0.65,
             font_size=28, bold=True, color=WHITE)
    if subtitle:
        add_text(slide, subtitle, 0.5, 0.78, 11, 0.42,
                 font_size=14, color=RGBColor(0xC0, 0xCF, 0xFF))
    # Accent line
    add_rect(slide, 0, 1.35, 13.33, 0.04, fill_rgb=ACCENT_BLUE)


def footer(slide, text="IBM MQ インフラ疎通確認  |  社外秘"):
    add_rect(slide, 0, 7.15, 13.33, 0.35, fill_rgb=IBM_BLUE)
    add_text(slide, text, 0.4, 7.17, 12, 0.28,
             font_size=9, color=RGBColor(0xB0, 0xBF, 0xFF))


def section_label(slide, text, l, t, w=2.6, h=0.32):
    add_rect(slide, l, t, w, h, fill_rgb=ACCENT_BLUE)
    add_text(slide, text, l+0.1, t+0.03, w-0.15, h-0.06,
             font_size=11, bold=True, color=WHITE)


# ══════════════════════════════════════════════════════════════════════════════
# Slide 1 – Title
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
# Full-bleed BG
add_rect(s, 0, 0, 13.33, 7.5, fill_rgb=IBM_BLUE)
add_rect(s, 0, 5.2, 13.33, 2.3, fill_rgb=RGBColor(0x03, 0x1E, 0x7A))

# Decorative accent shapes
add_rect(s, 9.8, 0, 0.18, 7.5, fill_rgb=ACCENT_BLUE)
add_rect(s, 10.1, 0, 0.06, 7.5, fill_rgb=RGBColor(0x00, 0x40, 0xBB))

# Title text
add_text(s, "IBM MQ", 1.0, 1.2, 9, 0.9,
         font_size=42, bold=True, color=RGBColor(0xC0, 0xCF, 0xFF))
add_text(s, "インフラ疎通確認", 1.0, 2.0, 9, 1.0,
         font_size=48, bold=True, color=WHITE)
add_text(s, "段取り・手順のご説明", 1.0, 3.0, 9, 0.6,
         font_size=24, color=RGBColor(0xC0, 0xCF, 0xFF))

add_rect(s, 1.0, 3.75, 4.5, 0.05, fill_rgb=ACCENT_BLUE)

add_text(s, "システム連携プロジェクト　2025年", 1.0, 4.0, 9, 0.5,
         font_size=16, color=RGBColor(0xB0, 0xBF, 0xFF))
add_text(s, "インフラ担当", 1.0, 4.5, 9, 0.45,
         font_size=14, color=RGBColor(0x90, 0xA8, 0xE8))

# ══════════════════════════════════════════════════════════════════════════════
# Slide 2 – Agenda
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
slide_bg(s)
header_bar(s, "アジェンダ", "本日ご説明する内容")
footer(s)

agenda_items = [
    ("01", "疎通確認の全体像",      "目的・フェーズ・担当分担"),
    ("02", "全体スケジュール",       "5月調整 → 6〜7月疎通実施"),
    ("03", "事前準備（依頼事項）",   "対向システムへの情報提供依頼"),
    ("04", "疎通確認 手順詳細",      "3フェーズの実施手順"),
    ("05", "エビデンス・完了基準",   "記録方法・合否判定"),
    ("06", "エラー発生時の対応",     "切り分けフロー・ログ確認"),
]

col_positions = [(0.5, 1.6), (0.5, 2.5), (0.5, 3.4),
                 (6.9, 1.6), (6.9, 2.5), (6.9, 3.4)]

for i, (num, title, desc) in enumerate(agenda_items):
    lx, ty = col_positions[i]
    add_rect(s, lx, ty, 5.9, 0.75, fill_rgb=WHITE,
             line_rgb=LIGHT_GRAY, line_width_pt=1)
    add_rect(s, lx, ty, 0.55, 0.75, fill_rgb=ACCENT_BLUE)
    add_text(s, num, lx+0.06, ty+0.15, 0.45, 0.45,
             font_size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, title, lx+0.65, ty+0.07, 5.1, 0.35,
             font_size=14, bold=True, color=DARK_TEXT)
    add_text(s, desc,  lx+0.65, ty+0.42, 5.1, 0.28,
             font_size=10, color=GRAY, italic=True)

# ══════════════════════════════════════════════════════════════════════════════
# Slide 3 – Overview
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
slide_bg(s)
header_bar(s, "疎通確認の全体像", "目的・フェーズ・担当分担")
footer(s)

add_text(s, "疎通確認はアプリ開発なしでインフラ担当レベルのみで実施します。",
         0.5, 1.55, 12, 0.4, font_size=13, color=DARK_TEXT)

# Phase boxes
phases = [
    ("①", "ネットワーク\n疎通確認", "ping / telnet / nc\nでポートへの到達確認", ACCENT_BLUE),
    ("②", "MQ接続\n確認",          "Channel接続確立\nQueueManagerへの接続", RGBColor(0x00, 0x82, 0xC8)),
    ("③", "メッセージ\n送受信確認", "amqsput / amqsget\nによるテストメッセージ", GREEN),
]

for i, (num, title, desc, col) in enumerate(phases):
    lx = 0.7 + i * 4.1
    add_rect(s, lx, 2.05, 3.6, 3.2, fill_rgb=col)
    add_rect(s, lx+0.15, 2.25, 3.3, 2.8, fill_rgb=WHITE,
             line_rgb=col, line_width_pt=0)
    add_rect(s, lx, 2.05, 3.6, 0.55, fill_rgb=col)
    add_text(s, f"フェーズ {num}", lx+0.15, 2.07, 3.3, 0.42,
             font_size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, title, lx+0.15, 2.65, 3.3, 0.9,
             font_size=18, bold=True, color=col, align=PP_ALIGN.CENTER)
    add_text(s, desc, lx+0.2, 3.55, 3.2, 0.9,
             font_size=12, color=DARK_TEXT, align=PP_ALIGN.CENTER)

    # Arrow between phases
    if i < 2:
        ax = lx + 3.65
        add_rect(s, ax, 3.35, 0.35, 0.3, fill_rgb=GRAY)
        add_text(s, "▶", ax+0.04, 3.3, 0.3, 0.38,
                 font_size=14, color=WHITE, align=PP_ALIGN.CENTER)

# Responsibility note
add_rect(s, 0.5, 5.45, 12.3, 0.9, fill_rgb=LIGHT_GRAY)
add_text(s, "【担当分担】　①ネットワーク疎通：双方のインフラ担当が連携して確認  ／  "
           "②③ MQ接続・メッセージ確認：こちら（新規側）インフラ担当が主導",
         0.65, 5.52, 12.0, 0.75, font_size=12, color=DARK_TEXT)

# ══════════════════════════════════════════════════════════════════════════════
# Slide 4 – Schedule (Gantt-style)
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
slide_bg(s)
header_bar(s, "全体スケジュール", "2025年5月〜7月")
footer(s)

months = ["5月", "6月", "7月"]
month_colors = [
    RGBColor(0xE8, 0xEC, 0xF5),
    RGBColor(0xD6, 0xE4, 0xFF),
    RGBColor(0xC6, 0xDD, 0xFF),
]

CHART_L = 3.5
CHART_T = 1.6
CHART_W = 9.2
CHART_H = 4.8
COL_W   = CHART_W / 3

# Month header cells
for mi, (mo, mc) in enumerate(zip(months, month_colors)):
    cx = CHART_L + mi * COL_W
    add_rect(s, cx, CHART_T, COL_W, 0.5, fill_rgb=IBM_BLUE)
    add_text(s, mo, cx, CHART_T+0.05, COL_W, 0.4,
             font_size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(s, cx, CHART_T+0.5, COL_W, CHART_H-0.5, fill_rgb=mc)

# Vertical grid lines
for mi in range(1, 3):
    cx = CHART_L + mi * COL_W
    add_rect(s, cx, CHART_T+0.5, 0.015, CHART_H-0.5,
             fill_rgb=RGBColor(0xB0, 0xBE, 0xDD))

# Row labels (left column)
tasks = [
    "接続パラメータ\n情報収集",
    "ファイアウォール\n開放申請",
    "MQ環境構築\n（新規側）",
    "疎通確認\n実施",
    "エビデンス\n提出・完了確認",
]
ROW_H  = (CHART_H - 0.5) / len(tasks)
LABEL_L = 0.2
LABEL_W = 3.1

for ri, task in enumerate(tasks):
    ry = CHART_T + 0.5 + ri * ROW_H
    bg = WHITE if ri % 2 == 0 else RGBColor(0xF8, 0xF9, 0xFF)
    add_rect(s, LABEL_L, ry, LABEL_W, ROW_H, fill_rgb=bg,
             line_rgb=LIGHT_GRAY, line_width_pt=0.5)
    add_text(s, task, LABEL_L+0.1, ry+0.02, LABEL_W-0.2, ROW_H-0.06,
             font_size=10.5, bold=True, color=DARK_TEXT)

# Gantt bars  (col_start, col_end in [0,3] fractions of month)
#   each tuple: (month_index_start, frac_start, month_index_end, frac_end, color, label)
bars = [
    # 情報収集: 全5月
    (0, 0.05, 0, 0.92, ACCENT_BLUE,  "情報収集・調整"),
    # FW申請: 5月中旬〜6月上旬
    (0, 0.45, 1, 0.3,  RGBColor(0x00, 0x82, 0xC8), "申請・開放作業"),
    # MQ環境構築: 5月下旬〜6月中旬
    (0, 0.65, 1, 0.55, RGBColor(0x49, 0x36, 0xE8), "MQ環境構築"),
    # 疎通確認: 6月中旬〜7月中旬
    (1, 0.5,  2, 0.6,  GREEN, "疎通確認実施"),
    # エビデンス: 7月中旬〜7月末
    (2, 0.55, 2, 0.95, RGBColor(0xF1, 0x6E, 0x28), "エビデンス提出"),
]

for ri, (ms, fs, me, fe, bc, label) in enumerate(bars):
    ry   = CHART_T + 0.5 + ri * ROW_H
    bar_l = CHART_L + ms * COL_W + fs * COL_W
    bar_r = CHART_L + me * COL_W + fe * COL_W
    bar_w = bar_r - bar_l
    bar_pad = ROW_H * 0.18
    add_rect(s, bar_l, ry + bar_pad, bar_w, ROW_H - bar_pad*2, fill_rgb=bc)
    if bar_w > 0.9:
        add_text(s, label,
                 bar_l + 0.07, ry + bar_pad + 0.02,
                 bar_w - 0.1, ROW_H - bar_pad*2 - 0.05,
                 font_size=9, bold=True, color=WHITE)

# Milestone diamonds
milestones = [
    (1, 0.05, "疎通開始"),
    (2, 0.95, "完了"),
]
for (mi, fr, mlabel) in milestones:
    mx = CHART_L + mi * COL_W + fr * COL_W
    # find row for "疎通確認"
    ri = 3
    ry = CHART_T + 0.5 + ri * ROW_H + ROW_H/2
    add_rect(s, mx-0.13, ry-0.14, 0.28, 0.28,
             fill_rgb=RGBColor(0xF1, 0xC2, 0x1B))
    add_text(s, "◆", mx-0.18, ry-0.2, 0.4, 0.4,
             font_size=14, color=RGBColor(0xF1, 0xC2, 0x1B), align=PP_ALIGN.CENTER)
    add_text(s, mlabel, mx-0.35, ry+0.15, 0.8, 0.28,
             font_size=8, bold=True, color=RGBColor(0xB0, 0x6A, 0x00),
             align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# Slide 5 – Pre-requisite info (table style)
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
slide_bg(s)
header_bar(s, "事前準備：対向からの情報収集", "5月中に入手が必要な情報（依頼事項）")
footer(s)

section_label(s, "接続パラメータ（必須）", 0.5, 1.55)
headers = ["項目", "内容", "記入欄（対向記入）"]
col_ws  = [3.2, 5.2, 4.1]
rows = [
    ["QueueManager名",       "接続先のQMgr名称",                   ""],
    ["ホスト / IPアドレス",   "MQリスナーが稼働するサーバー",       ""],
    ["ポート番号",            "MQリスナーポート（デフォルト1414）", ""],
    ["Channel名",             "Server-Connection Channel名",        ""],
    ["テスト用キュー名",      "amqsput / amqsget 用キュー名",       ""],
]
TBL_L = 0.5; TBL_T = 1.95; TBL_ROW_H = 0.45
col_starts = [TBL_L]
for w in col_ws[:-1]:
    col_starts.append(col_starts[-1] + w)

for ci, (hdr, cw) in enumerate(zip(headers, col_ws)):
    add_rect(s, col_starts[ci], TBL_T, cw, 0.38, fill_rgb=IBM_BLUE)
    add_text(s, hdr, col_starts[ci]+0.1, TBL_T+0.06, cw-0.15, 0.28,
             font_size=11, bold=True, color=WHITE)

for ri, row in enumerate(rows):
    ry = TBL_T + 0.38 + ri * TBL_ROW_H
    bg = WHITE if ri % 2 == 0 else LIGHT_GRAY
    for ci, (cell, cw) in enumerate(zip(row, col_ws)):
        add_rect(s, col_starts[ci], ry, cw, TBL_ROW_H,
                 fill_rgb=bg, line_rgb=LIGHT_GRAY, line_width_pt=0.5)
        add_text(s, cell, col_starts[ci]+0.1, ry+0.07, cw-0.15, TBL_ROW_H-0.1,
                 font_size=11, color=DARK_TEXT)

section_label(s, "セキュリティ確認", 0.5, 4.65)
sec_items = [
    ("TLS/SSL の要否",        "必要な場合は証明書の交換が別途必要"),
    ("認証（ID/PW）の要否",   "必要な場合はアカウント払い出し依頼"),
    ("IP制限の有無",          "こちらのIPアドレスを事前連携"),
]
for i, (item, note) in enumerate(sec_items):
    lx = 0.5 + i * 4.25
    add_rect(s, lx, 5.05, 4.0, 0.9, fill_rgb=WHITE,
             line_rgb=ACCENT_BLUE, line_width_pt=1)
    add_text(s, "□ " + item, lx+0.15, 5.1, 3.7, 0.38,
             font_size=11, bold=True, color=DARK_TEXT)
    add_text(s, note, lx+0.15, 5.45, 3.7, 0.45,
             font_size=9.5, color=GRAY, italic=True)

# ══════════════════════════════════════════════════════════════════════════════
# Slide 6 – Procedure Detail
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
slide_bg(s)
header_bar(s, "疎通確認 手順詳細", "3フェーズの実施ステップ")
footer(s)

phase_data = [
    ("① ネットワーク疎通", ACCENT_BLUE, [
        "ping で対向IPへの到達確認",
        "telnet / nc でMQポート（1414）への接続確認",
        "NG → ファイアウォール・ルーティング確認へ",
    ]),
    ("② MQ接続確認", RGBColor(0x00, 0x82, 0xC8), [
        "クライアント接続: MQSERVER環境変数をセット",
        "Server-to-Server: Sender Channelを起動・状態確認",
        "STATUS(RUNNING) を確認",
    ]),
    ("③ メッセージ送受信", GREEN, [
        "amqsput <キュー名> <QMgr名> でメッセージ送信",
        "amqsget <キュー名> <QMgr名> でメッセージ受信",
        "折り返し確認: 対向が受信後にREPLYキューへ返信",
    ]),
]

for col_i, (title, col, steps) in enumerate(phase_data):
    cx = 0.5 + col_i * 4.25
    add_rect(s, cx, 1.55, 4.0, 4.95, fill_rgb=WHITE,
             line_rgb=col, line_width_pt=1.5)
    add_rect(s, cx, 1.55, 4.0, 0.5, fill_rgb=col)
    add_text(s, title, cx+0.15, 1.58, 3.7, 0.42,
             font_size=13, bold=True, color=WHITE)

    for si, step in enumerate(steps):
        sy = 2.2 + si * 1.1
        add_rect(s, cx+0.15, sy, 0.35, 0.35,
                 fill_rgb=col)
        add_text(s, str(si+1), cx+0.15, sy+0.02, 0.35, 0.33,
                 font_size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_text(s, step, cx+0.58, sy, 3.25, 0.9,
                 font_size=11, color=DARK_TEXT, wrap=True)

# Tip box
add_rect(s, 0.5, 5.9, 12.3, 0.65, fill_rgb=RGBColor(0xFF, 0xF8, 0xE1))
add_rect(s, 0.5, 5.9, 0.08, 0.65, fill_rgb=AMBER)
add_text(s, "POINT  各フェーズはNG判明次第、次フェーズに進まず原因を特定してください。"
            "　ネットワーク問題はMQ設定より優先して解消が必要です。",
         0.7, 5.97, 12.0, 0.5, font_size=11, color=RGBColor(0x60, 0x40, 0x00))

# ══════════════════════════════════════════════════════════════════════════════
# Slide 7 – Evidence & Completion Criteria
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
slide_bg(s)
header_bar(s, "エビデンス・完了基準", "確認結果の記録と合否判定")
footer(s)

section_label(s, "確認結果チェックリスト", 0.5, 1.55)

cl_headers = ["フェーズ", "確認項目", "合格基準", "結果"]
cl_col_ws  = [1.5, 4.2, 5.0, 1.6]
cl_rows = [
    ["①", "ping 疎通",           "パケットロスなし・応答あり",         "OK / NG"],
    ["①", "ポート疎通",           "Connected / open と表示",            "OK / NG"],
    ["②", "Channel接続",          "STATUS(RUNNING) 確認",               "OK / NG"],
    ["②", "amqsput 送信",         "AMQSPUT0 end が表示される",           "OK / NG"],
    ["②", "amqsget 受信",         "送信メッセージが受信できる",          "OK / NG"],
    ["③", "往復確認",             "対向からの折り返しメッセージを受信", "OK/NG/対象外"],
]

cl_starts = [0.5]
for w in cl_col_ws[:-1]:
    cl_starts.append(cl_starts[-1] + w)
CL_T = 1.95; CL_ROW_H = 0.42

for ci, (hdr, cw) in enumerate(zip(cl_headers, cl_col_ws)):
    add_rect(s, cl_starts[ci], CL_T, cw, 0.38, fill_rgb=IBM_BLUE)
    add_text(s, hdr, cl_starts[ci]+0.1, CL_T+0.06, cw-0.15, 0.28,
             font_size=11, bold=True, color=WHITE)

for ri, row in enumerate(cl_rows):
    ry = CL_T + 0.38 + ri * CL_ROW_H
    bg = WHITE if ri % 2 == 0 else LIGHT_GRAY
    for ci, (cell, cw) in enumerate(zip(row, cl_col_ws)):
        add_rect(s, cl_starts[ci], ry, cw, CL_ROW_H,
                 fill_rgb=bg, line_rgb=LIGHT_GRAY, line_width_pt=0.5)
        fc = DARK_TEXT
        if ci == 3:
            fc = GREEN if "OK" in cell and "NG" not in cell else GRAY
        add_text(s, cell, cl_starts[ci]+0.1, ry+0.07, cw-0.15, CL_ROW_H-0.1,
                 font_size=10.5, color=fc)

section_label(s, "エビデンスとして保存するもの", 0.5, 5.45)
ev_items = [
    "① 各コマンドの実行結果（スクリーンショット or テキスト貼り付け）",
    "② チェックリストの記入済みシート",
    "③ 確認日時・実施者・対向担当者の記録",
]
for i, ev in enumerate(ev_items):
    add_text(s, ev, 0.65, 5.85 + i*0.3, 12.0, 0.3,
             font_size=11, color=DARK_TEXT)

# ══════════════════════════════════════════════════════════════════════════════
# Slide 8 – Troubleshooting
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank_layout)
slide_bg(s)
header_bar(s, "エラー発生時の対応", "切り分けフロー・よくあるエラーコード")
footer(s)

# Flow
flow_steps = [
    ("ping NG",       "ルーティング\nFW確認",       RGBColor(0xF0, 0x50, 0x30)),
    ("ポートNG",      "リスナー起動\nFW開放確認",   RGBColor(0xF0, 0x80, 0x20)),
    ("Channel NG",    "Channel名・\nTLS設定確認",    AMBER),
    ("メッセージNG",  "Queue名・\n権限確認",          GREEN),
]
section_label(s, "切り分けフロー", 0.5, 1.55)
for fi, (trigger, action, col) in enumerate(flow_steps):
    fx = 0.5 + fi * 3.2
    add_rect(s, fx, 2.0, 2.8, 0.55, fill_rgb=col)
    add_text(s, trigger, fx+0.1, 2.05, 2.6, 0.45,
             font_size=13, bold=True, color=WHITE)
    add_rect(s, fx+0.15, 2.6, 2.5, 0.85, fill_rgb=WHITE,
             line_rgb=col, line_width_pt=1.5)
    add_text(s, "→ " + action, fx+0.2, 2.65, 2.3, 0.75,
             font_size=11, color=DARK_TEXT)
    if fi < 3:
        add_text(s, "▶", fx+2.82, 2.13, 0.35, 0.38,
                 font_size=14, color=GRAY, align=PP_ALIGN.CENTER)

section_label(s, "よくあるエラーコード", 0.5, 3.65)
err_headers = ["エラーコード", "メッセージ概要", "主な原因", "対処"]
err_col_ws  = [1.8, 3.2, 3.5, 4.0]
err_rows = [
    ["AMQ9204", "Connection refused",       "ポート未開放 / リスナー未起動", "FW開放・リスナー起動確認"],
    ["AMQ9213", "Channel name error",       "Channel名の不一致",            "対向に正式名称を再確認"],
    ["AMQ9503", "Channel stopped",          "TLS設定の不一致",              "Cipher Suite を対向と合わせる"],
    ["AMQ2035", "Not authorized",           "認証エラー（ID/PW等）",        "MCA認証設定を確認"],
    ["AMQ9999", "Channel ended abnormally", "一般エラー",                   "/var/mqm/errors/ のログを確認"],
]
err_starts = [0.5]
for w in err_col_ws[:-1]:
    err_starts.append(err_starts[-1] + w)
ET = 4.05; ER_H = 0.38

for ci, (hdr, cw) in enumerate(zip(err_headers, err_col_ws)):
    add_rect(s, err_starts[ci], ET, cw, 0.35, fill_rgb=IBM_BLUE)
    add_text(s, hdr, err_starts[ci]+0.1, ET+0.04, cw-0.15, 0.28,
             font_size=10, bold=True, color=WHITE)

for ri, row in enumerate(err_rows):
    ry = ET + 0.35 + ri * ER_H
    bg = WHITE if ri % 2 == 0 else LIGHT_GRAY
    for ci, (cell, cw) in enumerate(zip(row, err_col_ws)):
        add_rect(s, err_starts[ci], ry, cw, ER_H,
                 fill_rgb=bg, line_rgb=LIGHT_GRAY, line_width_pt=0.5)
        add_text(s, cell, err_starts[ci]+0.1, ry+0.05, cw-0.15, ER_H-0.08,
                 font_size=9.5, color=DARK_TEXT)

# ══════════════════════════════════════════════════════════════════════════════
# Save
# ══════════════════════════════════════════════════════════════════════════════
out_path = "/home/user/ibm-mq/IBM_MQ_疎通確認_顧客説明資料.pptx"
prs.save(out_path)
print(f"Saved: {out_path}")
