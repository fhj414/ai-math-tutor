<template>
  <div class="student-bar">
    <select
      :value="currentStudentId"
      class="student-select"
      @change="onStudentChange"
    >
      <option v-for="item in studentList" :key="item.id" :value="item.id">
        {{ item.name }}
      </option>
    </select>

    <input
      :value="newStudentName"
      class="student-input"
      placeholder="输入新学生姓名"
      @input="onNameInput"
    />

    <button class="retry-btn" @click="$emit('create-student')">
      新增学生
    </button>

    <button class="wrong-btn" @click="$emit('export-report')">
      导出练习单
    </button>
  </div>
</template>

<script setup lang="ts">
import type { StudentItem } from '../api/math'

defineProps<{
  studentList: StudentItem[]
  currentStudentId: number
  newStudentName: string
}>()

const emit = defineEmits<{
  (e: 'update:currentStudentId', value: number): void
  (e: 'update:newStudentName', value: string): void
  (e: 'student-change'): void
  (e: 'create-student'): void
  (e: 'export-report'): void
}>()

const onStudentChange = (event: Event) => {
  const value = Number((event.target as HTMLSelectElement).value)
  emit('update:currentStudentId', value)
  emit('student-change')
}

const onNameInput = (event: Event) => {
  emit('update:newStudentName', (event.target as HTMLInputElement).value)
}
</script>

<style scoped>
.student-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 20px;
}

.student-select,
.student-input {
  height: 40px;
  padding: 0 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  outline: none;
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
</style>