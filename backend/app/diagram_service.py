import html
import json
import re
from typing import Any


def _find_number(text: str, pattern: str):
    match = re.search(pattern, text)
    return match.group(1) if match else None


def _build_hints(text: str, radius: str | None = None, angle: str | None = None):
    hints: list[str] = []

    if "面积" in text:
        hints.append(
            f"面积提示: S = π × {radius}²" if radius else "面积提示: S = πr²"
        )
    if "周长" in text:
        hints.append(
            f"周长提示: C = 2π × {radius}" if radius else "周长提示: C = 2πr"
        )
    if "弧长" in text or "扇形" in text:
        hints.append(
            f"弧长提示: l = {angle}/360 × 2π × {radius}"
            if radius and angle
            else "弧长提示: l = n/360 × 2πr"
        )

    return hints


def _build_annotations(text: str, steps: list[str]):
    source = f"{text} {' '.join(steps)}"
    annotations: list[str] = []

    if "对角线" in source and ("交于点O" in source or "交于O" in source or "点O" in source):
        annotations.append("标注点 O 为两条对角线的交点")
    if "对角线互相平分" in source:
        annotations.append("标注性质: 平行四边形对角线互相平分")
    if "中点" in source:
        annotations.append("标注性质: 图中涉及中点关系")
    if "直角" in source:
        annotations.append("标注角: 图中存在直角")

    return annotations


def get_diagram_data(question: str, steps: list[str] | None = None):
    text = re.sub(r"\s+", "", question or "")
    step_list = steps or []
    annotations = _build_annotations(text, step_list)

    if "扇形" in text:
        radius = _find_number(text, r"半径(?:是|为)?(\d+(?:\.\d+)?)") or _find_number(text, r"r=(\d+(?:\.\d+)?)")
        angle = _find_number(text, r"圆心角(?:是|为)?(\d+(?:\.\d+)?)") or _find_number(text, r"角(?:度)?(?:是|为)?(\d+(?:\.\d+)?)")
        return {
            "type": "sector",
            "title": "扇形示意图",
            "labels": [f"半径 {radius}" if radius else "半径 r", f"圆心角 {angle}°" if angle else "圆心角 θ"],
            "hints": _build_hints(text, radius, angle),
            "annotations": annotations,
        }

    if any(keyword in text for keyword in ["圆", "直径", "半径"]):
        radius = _find_number(text, r"半径(?:是|为)?(\d+(?:\.\d+)?)") or _find_number(text, r"r=(\d+(?:\.\d+)?)")
        diameter = _find_number(text, r"直径(?:是|为)?(\d+(?:\.\d+)?)")
        if not diameter and radius:
            diameter = str(float(radius) * 2).rstrip("0").rstrip(".")
        return {
            "type": "circle",
            "title": "圆形示意图",
            "labels": [f"半径 {radius}" if radius else "半径 r", f"直径 {diameter}" if diameter else "直径 d"],
            "hints": _build_hints(text, radius),
            "annotations": annotations,
        }

    if "正方形" in text:
        side = _find_number(text, r"边长(?:是|为)?(\d+(?:\.\d+)?)")
        hints = []
        if "面积" in text:
            hints.append(f"面积提示: S = {side} × {side}" if side else "面积提示: S = a²")
        if "周长" in text:
            hints.append(f"周长提示: C = 4 × {side}" if side else "周长提示: C = 4a")
        return {
            "type": "square",
            "title": "正方形示意图",
            "labels": [f"边长 {side}" if side else "边长 a"],
            "hints": hints,
            "annotations": annotations,
        }

    if "平行四边形" in text:
        base = _find_number(text, r"底(?:边)?(?:是|为)?(\d+(?:\.\d+)?)") or _find_number(text, r"AB=(\d+(?:\.\d+)?)")
        height = _find_number(text, r"高(?:是|为)?(\d+(?:\.\d+)?)")
        diagonal = _find_number(text, r"对角线(?:AC|BD)?(?:是|为)?(\d+(?:\.\d+)?)")
        hints = [f"面积提示: S = {base} × {height}" if base and height else "面积提示: S = 底 × 高"] if "面积" in text else []
        note_list = annotations + (["标注线段 AC、BD 为对角线"] if "对角线" in text else [])
        return {
            "type": "parallelogram",
            "title": "平行四边形示意图",
            "labels": [f"底 {base}" if base else "底 a", f"高 {height}" if height else "高 h", f"对角线 {diagonal}" if diagonal else "对角线"],
            "hints": hints,
            "annotations": note_list,
        }

    if "长方形" in text or "矩形" in text:
        length = _find_number(text, r"长(?:是|为)?(\d+(?:\.\d+)?)")
        width = _find_number(text, r"宽(?:是|为)?(\d+(?:\.\d+)?)")
        hints = []
        if "面积" in text:
            hints.append(f"面积提示: S = {length} × {width}" if length and width else "面积提示: S = ab")
        if "周长" in text:
            hints.append(f"周长提示: C = 2 × ({length} + {width})" if length and width else "周长提示: C = 2(a+b)")
        return {
            "type": "rectangle",
            "title": "矩形示意图",
            "labels": [f"长 {length}" if length else "长 a", f"宽 {width}" if width else "宽 b"],
            "hints": hints,
            "annotations": annotations,
        }

    if "梯形" in text:
        top_base = _find_number(text, r"上底(?:是|为)?(\d+(?:\.\d+)?)")
        bottom_base = _find_number(text, r"下底(?:是|为)?(\d+(?:\.\d+)?)")
        height = _find_number(text, r"高(?:是|为)?(\d+(?:\.\d+)?)")
        hints = []
        if "面积" in text:
            hints.append(
                f"面积提示: S = ({top_base} + {bottom_base}) × {height} ÷ 2"
                if top_base and bottom_base and height
                else "面积提示: S = (上底 + 下底) × 高 ÷ 2"
            )
        return {
            "type": "trapezoid",
            "title": "梯形示意图",
            "labels": [f"上底 {top_base}" if top_base else "上底 a", f"下底 {bottom_base}" if bottom_base else "下底 b", f"高 {height}" if height else "高 h"],
            "hints": hints,
            "annotations": annotations,
        }

    if any(keyword in text for keyword in ["三角形", "直角三角形", "等腰三角形"]):
        side_a = _find_number(text, r"边长(?:是|为)?(\d+(?:\.\d+)?)")
        side_b = _find_number(text, r"底(?:边)?(?:是|为)?(\d+(?:\.\d+)?)")
        hints = ["面积提示: S = 底 × 高 ÷ 2"] if "面积" in text else []
        return {
            "type": "triangle",
            "title": "三角形示意图",
            "labels": [f"边 {side_a}" if side_a else "边 a", f"底 {side_b}" if side_b else "底 b"],
            "hints": hints,
            "annotations": annotations,
        }

    if any(keyword in text for keyword in ["坐标系", "坐标平面", "点A", "点B", "x轴", "y轴", "原点"]):
        point_a_match = re.search(r"点A[（(]([^，。,；;)）]+)[)）]", text)
        point_b_match = re.search(r"点B[（(]([^，。,；;)）]+)[)）]", text)
        point_a = point_a_match.group(1) if point_a_match else None
        point_b = point_b_match.group(1) if point_b_match else None
        hints = ["坐标提示: 可用两点间距离公式"] if "距离" in text else []
        note_list = annotations + ([f"标注点 A 坐标为 {point_a}"] if point_a else [])
        return {
            "type": "coordinate",
            "title": "坐标系示意图",
            "labels": [f"A({point_a})" if point_a else "A(x1, y1)", f"B({point_b})" if point_b else "B(x2, y2)"],
            "hints": hints,
            "annotations": note_list,
        }

    return None


def render_diagram_html(question: str, steps: list[str] | None = None):
    diagram = get_diagram_data(question, steps)
    if not diagram:
        return ""

    labels_html = "".join(
        f'<span class="diagram-tag">{html.escape(label)}</span>'
        for label in diagram["labels"]
    )
    hints_html = "".join(
        f'<div class="diagram-note">{html.escape(hint)}</div>'
        for hint in diagram["hints"]
    )
    annotations_html = "".join(
        f'<div class="diagram-note subtle">{html.escape(annotation)}</div>'
        for annotation in diagram["annotations"]
    )

    svg_map: dict[str, str] = {
        "circle": """
          <svg viewBox="0 0 220 150" class="diagram-svg" aria-label="圆形示意图">
            <circle cx="110" cy="78" r="46" class="shape-fill" />
            <line x1="110" y1="78" x2="156" y2="78" class="shape-line dashed" />
            <line x1="64" y1="78" x2="156" y2="78" class="shape-line" />
            <text x="162" y="83" class="shape-text">r</text>
            <text x="104" y="64" class="shape-text">O</text>
          </svg>
        """,
        "sector": """
          <svg viewBox="0 0 220 150" class="diagram-svg" aria-label="扇形示意图">
            <path d="M110 80 L160 80 A50 50 0 0 0 145 42 Z" class="shape-fill" />
            <line x1="110" y1="80" x2="160" y2="80" class="shape-line" />
            <line x1="110" y1="80" x2="145" y2="42" class="shape-line" />
            <text x="112" y="76" class="shape-text">O</text>
            <text x="151" y="92" class="shape-text">r</text>
            <text x="126" y="67" class="shape-text">θ</text>
          </svg>
        """,
        "square": """
          <svg viewBox="0 0 220 150" class="diagram-svg" aria-label="正方形示意图">
            <rect x="60" y="30" width="90" height="90" rx="8" class="shape-fill" />
            <line x1="60" y1="130" x2="150" y2="130" class="shape-line" />
            <text x="100" y="146" class="shape-text">a</text>
          </svg>
        """,
        "parallelogram": """
          <svg viewBox="0 0 220 150" class="diagram-svg" aria-label="平行四边形示意图">
            <polygon points="62,36 156,36 188,112 94,112" class="shape-fill" />
            <line x1="62" y1="36" x2="188" y2="112" class="shape-line dashed" />
            <line x1="156" y1="36" x2="94" y2="112" class="shape-line dashed" />
            <circle cx="125" cy="74" r="4" class="point-fill" />
            <text x="56" y="32" class="shape-text">A</text>
            <text x="158" y="32" class="shape-text">B</text>
            <text x="190" y="120" class="shape-text">C</text>
            <text x="84" y="124" class="shape-text">D</text>
            <text x="131" y="70" class="shape-text">O</text>
          </svg>
        """,
        "rectangle": """
          <svg viewBox="0 0 220 150" class="diagram-svg" aria-label="矩形示意图">
            <rect x="48" y="36" width="124" height="76" rx="8" class="shape-fill" />
            <line x1="48" y1="120" x2="172" y2="120" class="shape-line" />
            <line x1="180" y1="36" x2="180" y2="112" class="shape-line" />
            <text x="104" y="138" class="shape-text">长</text>
            <text x="186" y="80" class="shape-text">宽</text>
          </svg>
        """,
        "trapezoid": """
          <svg viewBox="0 0 220 150" class="diagram-svg" aria-label="梯形示意图">
            <polygon points="70,36 150,36 182,112 38,112" class="shape-fill" />
            <line x1="70" y1="126" x2="150" y2="126" class="shape-line" />
            <line x1="186" y1="36" x2="186" y2="112" class="shape-line dashed" />
            <text x="102" y="142" class="shape-text">下底</text>
            <text x="190" y="78" class="shape-text">高</text>
          </svg>
        """,
        "coordinate": """
          <svg viewBox="0 0 220 150" class="diagram-svg" aria-label="坐标系示意图">
            <line x1="30" y1="118" x2="190" y2="118" class="shape-line" />
            <line x1="56" y1="134" x2="56" y2="18" class="shape-line" />
            <line x1="56" y1="118" x2="128" y2="54" class="shape-line dashed" />
            <circle cx="56" cy="118" r="4" class="point-fill" />
            <circle cx="128" cy="54" r="4" class="point-fill" />
            <text x="194" y="122" class="shape-text">x</text>
            <text x="60" y="22" class="shape-text">y</text>
            <text x="44" y="132" class="shape-text">O</text>
            <text x="132" y="48" class="shape-text">A</text>
          </svg>
        """,
        "triangle": """
          <svg viewBox="0 0 220 150" class="diagram-svg" aria-label="三角形示意图">
            <polygon points="110,24 40,116 180,116" class="shape-fill" />
            <line x1="110" y1="24" x2="40" y2="116" class="shape-line" />
            <line x1="110" y1="24" x2="180" y2="116" class="shape-line" />
            <line x1="40" y1="116" x2="180" y2="116" class="shape-line" />
            <text x="108" y="18" class="shape-text">A</text>
            <text x="28" y="128" class="shape-text">B</text>
            <text x="184" y="128" class="shape-text">C</text>
          </svg>
        """,
    }

    hint_section = f'<div class="diagram-notes">{hints_html}</div>' if hints_html else ""
    annotation_section = (
        f'<div class="diagram-annotations"><div class="diagram-annotations-title">解析标注</div>{annotations_html}</div>'
        if annotations_html
        else ""
    )

    return f"""
      <div class="diagram-card">
        <div class="diagram-header">
          <strong>{html.escape(diagram["title"])}</strong>
          <div class="diagram-labels">{labels_html}</div>
        </div>
        {svg_map.get(diagram["type"], "")}
        {hint_section}
        {annotation_section}
      </div>
    """


def parse_paper_payload(payload: str | None) -> dict[str, Any] | None:
    if not payload:
        return None

    return json.loads(payload)
