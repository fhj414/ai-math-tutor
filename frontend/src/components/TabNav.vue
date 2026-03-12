<template>
  <div class="tabs">
    <button
      v-for="item in tabList"
      :key="item.value"
      :class="['tab-btn', activeTab === item.value ? 'active' : '']"
      @click="$emit('change', item.value)"
    >
      {{ item.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  activeTab: 'solve' | 'history' | 'wrong' | 'report' | 'suggestion'
}>()

defineEmits<{
  (e: 'change', value: 'solve' | 'history' | 'wrong' | 'report' | 'suggestion'): void
}>()

const tabList = [
  { label: '题目解析', value: 'solve' },
  { label: '历史记录', value: 'history' },
  { label: '错题本', value: 'wrong' },
  { label: '学习报告', value: 'report' },
  { label: '学习建议', value: 'suggestion' },
] as const
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.tab-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
}

.tab-btn.active {
  background: #18a058;
  color: #fff;
  border-color: #18a058;
}
</style>