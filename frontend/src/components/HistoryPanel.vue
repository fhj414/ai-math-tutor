<template>
  <div>
    <div v-if="historyList.length === 0" class="empty">暂无历史记录</div>

    <div v-for="item in historyList" :key="item.id" class="result-card">
      <div class="card-header">
        <h2>记录 #{{ item.id }}</h2>

        <div class="card-actions">
          <button class="retry-btn" @click="$emit('regenerate', item.id)">
            {{ regenerateLoadingMap[item.id] ? '生成中...' : '再练一题' }}
          </button>

          <button class="wrong-btn" @click="$emit('toggle-wrong', item)">
            {{ item.is_wrong ? '取消错题' : '加入错题本' }}
          </button>
        </div>
      </div>

      <h3>题目</h3>
      <p>{{ item.question }}</p>
      <MathDiagram :question="item.question" :steps="item.steps" />

      <h3>答案</h3>
      <p>{{ item.answer }}</p>

      <h3>步骤解析</h3>
      <ol>
        <li v-for="(step, idx) in item.steps" :key="idx">{{ step }}</li>
      </ol>

      <h3>知识点</h3>
      <ul>
        <li v-for="(kp, idx) in item.knowledge_points" :key="idx">{{ kp }}</li>
      </ul>

      <h3>相似题</h3>
      <p>{{ item.similar_question }}</p>

      <div v-if="regeneratedMap[item.id]" class="regenerated-box">
        <h3>再练一题</h3>
        <p>{{ regeneratedMap[item.id]?.question }}</p>
        <MathDiagram
          v-if="regeneratedMap[item.id]?.question"
          :question="regeneratedMap[item.id]?.question ?? ''"
          :steps="regeneratedMap[item.id]?.steps ?? []"
        />

        <h3>答案</h3>
        <p>{{ regeneratedMap[item.id]?.answer }}</p>

        <h3>步骤解析</h3>
        <ol>
          <li v-for="(step, idx) in regeneratedMap[item.id]?.steps ?? []" :key="idx">
            {{ step }}
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MathDiagram from './MathDiagram.vue'
import type { HistoryItem, PracticeQuestionItem } from '../api/math'

defineProps<{
  historyList: HistoryItem[]
  regenerateLoadingMap: Record<number, boolean>
  regeneratedMap: Record<number, PracticeQuestionItem>
}>()

defineEmits<{
  (e: 'toggle-wrong', item: HistoryItem): void
  (e: 'regenerate', id: number): void
}>()
</script>

<style scoped>
.empty {
  padding: 32px 0;
  text-align: center;
  color: #999;
}

.result-card {
  margin-top: 24px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.retry-btn {
  padding: 8px 14px;
  border: none;
  background: #2080f0;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
}

.wrong-btn {
  padding: 8px 14px;
  border: none;
  background: #f0a020;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
}

.regenerated-box {
  margin-top: 16px;
  padding: 16px;
  background: #f0f7ff;
  border-radius: 8px;
}

@media (max-width: 520px) {
  .retry-btn,
  .wrong-btn {
    width: 100%;
  }
}
</style>
