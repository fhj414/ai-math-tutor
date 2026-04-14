<template>
  <div class="paper-panel">
    <div class="result-card">
      <h2>AI 自动出卷</h2>

      <div class="paper-form">
        <input
          :value="knowledgePoint"
          class="paper-input"
          placeholder="请输入知识点，例如：一元一次方程"
          @input="$emit('update:knowledgePoint', ($event.target as HTMLInputElement).value)"
        />

        <input
          :value="count"
          class="paper-count"
          type="number"
          min="1"
          max="20"
          @input="$emit('update:count', Number(($event.target as HTMLInputElement).value))"
        />

        <select
          :value="difficulty"
          class="paper-select"
          @change="$emit('update:difficulty', ($event.target as HTMLSelectElement).value)"
        >
          <option value="简单">简单</option>
          <option value="中等">中等</option>
          <option value="困难">困难</option>
        </select>

        <button class="submit-btn" :disabled="loading" @click="$emit('generate')">
          {{ loading ? '生成中...' : '生成试卷' }}
        </button>

        <label class="paper-checkbox">
          <input
            :checked="preferDiagram"
            type="checkbox"
            @change="$emit('update:preferDiagram', ($event.target as HTMLInputElement).checked)"
          />
          优先生成带图几何题
        </label>

        <button class="retry-btn" @click="$emit('export')">
          导出试卷
        </button>
      </div>
    </div>

    <div v-if="paper" class="result-card">
      <h2>{{ paper.knowledge_point }} 专项练习卷</h2>
      <p><strong>难度：</strong>{{ paper.difficulty }}</p>

      <div v-for="(item, index) in paper.questions" :key="index" class="paper-question">
        <h3>第 {{ index + 1 }} 题</h3>
        <p>{{ item.question }}</p>
        <MathDiagram :question="item.question" :steps="item.steps" />

        <h4>答案</h4>
        <p>{{ item.answer }}</p>

        <h4>解析</h4>
        <ol>
          <li v-for="(step, idx) in item.steps" :key="idx">{{ step }}</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MathDiagram from './MathDiagram.vue'
import type { GeneratePaperResponse } from '../api/math'

defineProps<{
  knowledgePoint: string
  count: number
  difficulty: string
  preferDiagram: boolean
  loading: boolean
  paper: GeneratePaperResponse | null
}>()

defineEmits<{
  (e: 'update:knowledgePoint', value: string): void
  (e: 'update:count', value: number): void
  (e: 'update:difficulty', value: string): void
  (e: 'update:preferDiagram', value: boolean): void
  (e: 'generate'): void
  (e: 'export'): void
}>()
</script>

<style scoped>
.paper-panel {
  margin-top: 24px;
}

.paper-form {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.paper-input,
.paper-count,
.paper-select {
  height: 40px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  background: #fff;
}

.paper-checkbox {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 40px;
  padding: 0 4px;
  color: #31475e;
}

.paper-input {
  flex: 1;
  min-width: 240px;
}

.paper-count {
  width: 100px;
}

.submit-btn {
  padding: 10px 18px;
  border: none;
  background: #18a058;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
}

.retry-btn {
  padding: 10px 18px;
  border: none;
  background: #2080f0;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
}

.result-card {
  margin-top: 24px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.paper-question {
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}

@media (max-width: 520px) {
  .paper-form > * {
    width: 100%;
  }

  .paper-input,
  .paper-count,
  .paper-select,
  .submit-btn,
  .retry-btn {
    width: 100%;
  }
}
</style>
