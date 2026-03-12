<template>
  <div>
    <div class="upload-area">
      <label class="upload-btn">
        {{ imageLoading ? '识别中...' : '上传题目图片' }}
        <input
          type="file"
          accept="image/*"
          class="file-input"
          :disabled="imageLoading"
          @change="$emit('image-change', $event)"
        />
      </label>
    </div>

    <textarea
      :value="question"
      class="question-input"
      placeholder="请输入一道数学题，例如：解方程 3x + 5 = 11"
      @input="$emit('update:question', ($event.target as HTMLTextAreaElement).value)"
    />

    <button class="submit-btn" @click="$emit('submit')" :disabled="loading">
      {{ loading ? '解析中...' : '开始解析' }}
    </button>

    <div v-if="result" class="result-card">
      <div class="card-header">
        <h2>本次解析结果</h2>

        <div class="card-actions">
          <button class="retry-btn" @click="$emit('regenerate', result.id)">
            {{ regenerateLoadingMap[result.id] ? '生成中...' : '再练一题' }}
          </button>

          <button class="wrong-btn" @click="$emit('toggle-wrong', result)">
            {{ result.is_wrong ? '取消错题' : '加入错题本' }}
          </button>
        </div>
      </div>

      <h3>题目</h3>
      <p>{{ result.question }}</p>

      <h3>答案</h3>
      <p>{{ result.answer }}</p>

      <h3>步骤解析</h3>
      <ol>
        <li v-for="(step, index) in result.steps" :key="index">{{ step }}</li>
      </ol>

      <h3>知识点</h3>
      <ul>
        <li v-for="(kp, index) in result.knowledge_points" :key="index">{{ kp }}</li>
      </ul>

      <h3>相似题</h3>
      <p>{{ result.similar_question }}</p>

      <div v-if="regeneratedMap[result.id]" class="regenerated-box">
        <h3>再练一题</h3>
        <p>{{ regeneratedMap[result.id].question }}</p>

        <h3>答案</h3>
        <p>{{ regeneratedMap[result.id].answer }}</p>

        <h3>步骤解析</h3>
        <ol>
          <li v-for="(step, idx) in regeneratedMap[result.id].steps" :key="idx">
            {{ step }}
          </li>
        </ol>
      </div>
    </div>

    <div class="practice-panel">
      <h2>按知识点生成练习题</h2>
      <div class="practice-form">
        <input
          :value="practiceKnowledge"
          class="practice-input"
          placeholder="请输入知识点，例如：一元一次方程"
          @input="$emit('update:practiceKnowledge', ($event.target as HTMLInputElement).value)"
        />
        <button class="submit-btn" @click="$emit('generate-practice')" :disabled="practiceLoading">
          {{ practiceLoading ? '生成中...' : '生成练习题' }}
        </button>
      </div>

      <div v-if="practiceList.length" class="practice-list">
        <div v-for="(item, index) in practiceList" :key="index" class="result-card">
          <h3>练习题 {{ index + 1 }}</h3>
          <p>{{ item.question }}</p>

          <h3>答案</h3>
          <p>{{ item.answer }}</p>

          <h3>步骤解析</h3>
          <ol>
            <li v-for="(step, idx) in item.steps" :key="idx">{{ step }}</li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PracticeQuestionItem, SolveResponse } from '../api/math'

defineProps<{
  question: string
  loading: boolean
  imageLoading: boolean
  result: (SolveResponse & { question: string }) | null
  practiceKnowledge: string
  practiceLoading: boolean
  practiceList: PracticeQuestionItem[]
  regenerateLoadingMap: Record<number, boolean>
  regeneratedMap: Record<number, PracticeQuestionItem>
}>()

defineEmits<{
  (e: 'update:question', value: string): void
  (e: 'submit'): void
  (e: 'image-change', event: Event): void
  (e: 'toggle-wrong', item: SolveResponse & { question: string }): void
  (e: 'regenerate', id: number): void
  (e: 'update:practiceKnowledge', value: string): void
  (e: 'generate-practice'): void
}>()
</script>

<style scoped>
.upload-area {
  margin-bottom: 16px;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  padding: 10px 16px;
  background: #2080f0;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
}

.file-input {
  display: none;
}

.question-input {
  width: 100%;
  min-height: 140px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-size: 16px;
  box-sizing: border-box;
}

.submit-btn {
  margin-top: 16px;
  padding: 10px 18px;
  border: none;
  background: #18a058;
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

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-actions {
  display: flex;
  gap: 8px;
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

.practice-panel {
  margin-top: 32px;
}

.practice-form {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.practice-input {
  flex: 1;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
}

.practice-list {
  margin-top: 16px;
}

.regenerated-box {
  margin-top: 16px;
  padding: 16px;
  background: #f0f7ff;
  border-radius: 8px;
}
</style>