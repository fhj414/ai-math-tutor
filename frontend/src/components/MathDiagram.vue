<template>
  <div v-if="diagram" class="diagram-card">
    <div class="diagram-header">
      <strong>{{ diagram.title }}</strong>
      <div class="diagram-labels">
        <span v-for="label in diagram.labels" :key="label" class="diagram-tag">
          {{ label }}
        </span>
      </div>
    </div>

    <svg
      v-if="diagram.type === 'circle'"
      viewBox="0 0 220 150"
      class="diagram-svg"
      aria-label="圆形示意图"
    >
      <circle cx="110" cy="78" r="46" class="shape-fill" />
      <line x1="110" y1="78" x2="156" y2="78" class="shape-line dashed" />
      <line x1="64" y1="78" x2="156" y2="78" class="shape-line" />
      <text x="162" y="83" class="shape-text">r</text>
      <text x="104" y="64" class="shape-text">O</text>
    </svg>

    <svg
      v-else-if="diagram.type === 'sector'"
      viewBox="0 0 220 150"
      class="diagram-svg"
      aria-label="扇形示意图"
    >
      <path d="M110 80 L160 80 A50 50 0 0 0 145 42 Z" class="shape-fill" />
      <line x1="110" y1="80" x2="160" y2="80" class="shape-line" />
      <line x1="110" y1="80" x2="145" y2="42" class="shape-line" />
      <text x="112" y="76" class="shape-text">O</text>
      <text x="151" y="92" class="shape-text">r</text>
      <text x="126" y="67" class="shape-text">θ</text>
    </svg>

    <svg
      v-else-if="diagram.type === 'square'"
      viewBox="0 0 220 150"
      class="diagram-svg"
      aria-label="正方形示意图"
    >
      <rect x="60" y="30" width="90" height="90" rx="8" class="shape-fill" />
      <line x1="60" y1="130" x2="150" y2="130" class="shape-line" />
      <text x="100" y="146" class="shape-text">a</text>
    </svg>

    <svg
      v-else-if="diagram.type === 'parallelogram'"
      viewBox="0 0 220 150"
      class="diagram-svg"
      aria-label="平行四边形示意图"
    >
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

    <svg
      v-else-if="diagram.type === 'rectangle'"
      viewBox="0 0 220 150"
      class="diagram-svg"
      aria-label="矩形示意图"
    >
      <rect x="48" y="36" width="124" height="76" rx="8" class="shape-fill" />
      <line x1="48" y1="120" x2="172" y2="120" class="shape-line" />
      <line x1="180" y1="36" x2="180" y2="112" class="shape-line" />
      <text x="104" y="138" class="shape-text">长</text>
      <text x="186" y="80" class="shape-text">宽</text>
    </svg>

    <svg
      v-else-if="diagram.type === 'trapezoid'"
      viewBox="0 0 220 150"
      class="diagram-svg"
      aria-label="梯形示意图"
    >
      <polygon points="70,36 150,36 182,112 38,112" class="shape-fill" />
      <line x1="70" y1="126" x2="150" y2="126" class="shape-line" />
      <line x1="186" y1="36" x2="186" y2="112" class="shape-line dashed" />
      <text x="102" y="142" class="shape-text">下底</text>
      <text x="190" y="78" class="shape-text">高</text>
    </svg>

    <svg
      v-else-if="diagram.type === 'coordinate'"
      viewBox="0 0 220 150"
      class="diagram-svg"
      aria-label="坐标系示意图"
    >
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

    <svg
      v-else
      viewBox="0 0 220 150"
      class="diagram-svg"
      aria-label="三角形示意图"
    >
      <polygon points="110,24 40,116 180,116" class="shape-fill" />
      <line x1="110" y1="24" x2="40" y2="116" class="shape-line" />
      <line x1="110" y1="24" x2="180" y2="116" class="shape-line" />
      <line x1="40" y1="116" x2="180" y2="116" class="shape-line" />
      <text x="108" y="18" class="shape-text">A</text>
      <text x="28" y="128" class="shape-text">B</text>
      <text x="184" y="128" class="shape-text">C</text>
    </svg>

    <div v-if="diagram.hints.length" class="diagram-notes">
      <div v-for="hint in diagram.hints" :key="hint" class="diagram-note">
        {{ hint }}
      </div>
    </div>

    <div v-if="diagram.annotations.length" class="diagram-annotations">
      <div class="diagram-annotations-title">解析标注</div>
      <div v-for="annotation in diagram.annotations" :key="annotation" class="diagram-note subtle">
        {{ annotation }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { getDiagramData } from "../utils/mathDiagram";

const props = defineProps<{
  question: string;
  steps?: string[];
}>();

const diagram = computed(() => getDiagramData(props.question, props.steps ?? []));
</script>

<style scoped>
.diagram-card {
  margin: 12px 0 18px;
  padding: 14px;
  border-radius: 14px;
  background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 100%);
  border: 1px solid #dbe8f6;
}

.diagram-header {
  display: flex;
  gap: 10px;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.diagram-labels {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.diagram-tag {
  padding: 4px 10px;
  border-radius: 999px;
  background: #fff;
  color: #36506b;
  font-size: 12px;
}

.diagram-svg {
  width: 100%;
  max-width: 320px;
  height: auto;
  display: block;
  margin-top: 12px;
}

.diagram-notes,
.diagram-annotations {
  margin-top: 12px;
  display: grid;
  gap: 8px;
}

.diagram-annotations-title {
  font-size: 13px;
  font-weight: 700;
  color: #36506b;
}

.diagram-note {
  padding: 8px 10px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.88);
  color: #31475e;
  font-size: 13px;
}

.diagram-note.subtle {
  background: rgba(227, 239, 251, 0.9);
}

.shape-fill {
  fill: rgba(32, 128, 240, 0.1);
  stroke: #2080f0;
  stroke-width: 3;
}

.shape-line {
  stroke: #f08c00;
  stroke-width: 3;
}

.shape-line.dashed {
  stroke-dasharray: 5 4;
}

.shape-text {
  fill: #22354a;
  font-size: 14px;
  font-weight: 700;
}

.point-fill {
  fill: #f08c00;
}
</style>
