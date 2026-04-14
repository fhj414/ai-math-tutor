export interface DiagramData {
  type: "circle" | "sector" | "rectangle" | "square" | "trapezoid" | "triangle" | "coordinate" | "parallelogram";
  title: string;
  labels: string[];
  hints: string[];
  annotations: string[];
}

function findNumber(question: string, pattern: RegExp) {
  const match = question.match(pattern);
  return match?.[1] ?? null;
}

function getCircleHints(text: string, radius: string | null, angle: string | null = null) {
  const hints: string[] = [];

  if (/面积/.test(text)) {
    hints.push(radius ? `面积提示: S = π × ${radius}²` : "面积提示: S = πr²");
  }

  if (/周长/.test(text)) {
    hints.push(radius ? `周长提示: C = 2π × ${radius}` : "周长提示: C = 2πr");
  }

  if (/弧长/.test(text) || /扇形/.test(text)) {
    hints.push(
      radius && angle
        ? `弧长提示: l = ${angle}/360 × 2π × ${radius}`
        : "弧长提示: l = n/360 × 2πr",
    );
  }

  return hints;
}

function getAnnotations(text: string, steps: string[] = []) {
  const source = `${text} ${steps.join(" ")}`;
  const annotations: string[] = [];

  if (/对角线/.test(source) && /交于点O|交于O|点O/.test(source)) {
    annotations.push("标注点 O 为两条对角线的交点");
  }

  if (/对角线互相平分/.test(source)) {
    annotations.push("标注性质: 平行四边形对角线互相平分");
  }

  if (/中点/.test(source)) {
    annotations.push("标注性质: 图中涉及中点关系");
  }

  if (/直角/.test(source)) {
    annotations.push("标注角: 图中存在直角");
  }

  return annotations;
}

export function getDiagramData(question: string, steps: string[] = []): DiagramData | null {
  const text = question.replace(/\s+/g, "");
  const annotations = getAnnotations(text, steps);

  if (/扇形/.test(text)) {
    const radius =
      findNumber(text, /半径(?:是|为)?(\d+(?:\.\d+)?)/) ||
      findNumber(text, /r=(\d+(?:\.\d+)?)/i);
    const angle =
      findNumber(text, /圆心角(?:是|为)?(\d+(?:\.\d+)?)/) ||
      findNumber(text, /角(?:度)?(?:是|为)?(\d+(?:\.\d+)?)/);

    return {
      type: "sector",
      title: "扇形示意图",
      labels: [
        radius ? `半径 ${radius}` : "半径 r",
        angle ? `圆心角 ${angle}°` : "圆心角 θ",
      ],
      hints: getCircleHints(text, radius, angle),
      annotations,
    };
  }

  if (/圆|直径|半径/.test(text)) {
    const radius =
      findNumber(text, /半径(?:是|为)?(\d+(?:\.\d+)?)/) ||
      findNumber(text, /r=(\d+(?:\.\d+)?)/i);
    const diameter =
      findNumber(text, /直径(?:是|为)?(\d+(?:\.\d+)?)/) ||
      (radius ? String(Number(radius) * 2) : null);

    return {
      type: "circle",
      title: "圆形示意图",
      labels: [
        radius ? `半径 ${radius}` : "半径 r",
        diameter ? `直径 ${diameter}` : "直径 d",
      ],
      hints: getCircleHints(text, radius),
      annotations,
    };
  }

  if (/正方形/.test(text)) {
    const side = findNumber(text, /边长(?:是|为)?(\d+(?:\.\d+)?)/);

    return {
      type: "square",
      title: "正方形示意图",
      labels: [side ? `边长 ${side}` : "边长 a"],
      hints: /面积/.test(text)
        ? [side ? `面积提示: S = ${side} × ${side}` : "面积提示: S = a²"]
        : /周长/.test(text)
          ? [side ? `周长提示: C = 4 × ${side}` : "周长提示: C = 4a"]
          : [],
      annotations,
    };
  }

  if (/长方形|矩形/.test(text)) {
    const length = findNumber(text, /长(?:是|为)?(\d+(?:\.\d+)?)/);
    const width = findNumber(text, /宽(?:是|为)?(\d+(?:\.\d+)?)/);

    return {
      type: "rectangle",
      title: "矩形示意图",
      labels: [
        length ? `长 ${length}` : "长 a",
        width ? `宽 ${width}` : "宽 b",
      ],
      hints: /面积/.test(text)
        ? [length && width ? `面积提示: S = ${length} × ${width}` : "面积提示: S = ab"]
        : /周长/.test(text)
          ? [length && width ? `周长提示: C = 2 × (${length} + ${width})` : "周长提示: C = 2(a+b)"]
          : [],
      annotations,
    };
  }

  if (/平行四边形/.test(text)) {
    const base = findNumber(text, /底(?:边)?(?:是|为)?(\d+(?:\.\d+)?)/) || findNumber(text, /AB=(\d+(?:\.\d+)?)/);
    const height = findNumber(text, /高(?:是|为)?(\d+(?:\.\d+)?)/);
    const diagonal = findNumber(text, /对角线(?:AC|BD)?(?:是|为)?(\d+(?:\.\d+)?)/);

    return {
      type: "parallelogram",
      title: "平行四边形示意图",
      labels: [
        base ? `底 ${base}` : "底 a",
        height ? `高 ${height}` : "高 h",
        diagonal ? `对角线 ${diagonal}` : "对角线",
      ],
      hints: /面积/.test(text)
        ? [base && height ? `面积提示: S = ${base} × ${height}` : "面积提示: S = 底 × 高"]
        : [],
      annotations: annotations.concat(/对角线/.test(text) ? ["标注线段 AC、BD 为对角线"] : []),
    };
  }

  if (/梯形/.test(text)) {
    const topBase = findNumber(text, /上底(?:是|为)?(\d+(?:\.\d+)?)/);
    const bottomBase = findNumber(text, /下底(?:是|为)?(\d+(?:\.\d+)?)/);
    const height = findNumber(text, /高(?:是|为)?(\d+(?:\.\d+)?)/);

    return {
      type: "trapezoid",
      title: "梯形示意图",
      labels: [
        topBase ? `上底 ${topBase}` : "上底 a",
        bottomBase ? `下底 ${bottomBase}` : "下底 b",
        height ? `高 ${height}` : "高 h",
      ],
      hints: /面积/.test(text)
        ? [
            topBase && bottomBase && height
              ? `面积提示: S = (${topBase} + ${bottomBase}) × ${height} ÷ 2`
              : "面积提示: S = (上底 + 下底) × 高 ÷ 2",
          ]
        : [],
      annotations,
    };
  }

  if (/三角形|直角三角形|等腰三角形/.test(text)) {
    const sideA = findNumber(text, /边长(?:是|为)?(\d+(?:\.\d+)?)/);
    const sideB = findNumber(text, /底(?:边)?(?:是|为)?(\d+(?:\.\d+)?)/);

    return {
      type: "triangle",
      title: "三角形示意图",
      labels: [
        sideA ? `边 ${sideA}` : "边 a",
        sideB ? `底 ${sideB}` : "底 b",
      ],
      hints: /面积/.test(text)
        ? [sideB ? "面积提示: S = 底 × 高 ÷ 2" : "面积提示: S = 底 × 高 ÷ 2"]
        : [],
      annotations,
    };
  }

  if (/坐标系|坐标平面|点A|点B|x轴|y轴|原点/.test(text)) {
    const pointA = text.match(/点A[（(]([^，。,；;)）]+)[)）]/)?.[1] ?? null;
    const pointB = text.match(/点B[（(]([^，。,；;)）]+)[)）]/)?.[1] ?? null;

    return {
      type: "coordinate",
      title: "坐标系示意图",
      labels: [
        pointA ? `A(${pointA})` : "A(x1, y1)",
        pointB ? `B(${pointB})` : "B(x2, y2)",
      ],
      hints: /距离/.test(text) ? ["坐标提示: 可用两点间距离公式"] : [],
      annotations: annotations.concat(pointA ? [`标注点 A 坐标为 ${pointA}`] : []),
    };
  }

  return null;
}
