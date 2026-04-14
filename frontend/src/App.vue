<template>
  <div class="page">
    <div class="container">
      <h1>AI 数学辅导老师</h1>

      <StudentBar
        v-model:currentStudentId="currentStudentId"
        v-model:newStudentName="newStudentName"
        :student-list="studentList"
        @student-change="handleStudentChange"
        @create-student="handleCreateStudent"
        @export-report="handleExportReport"
        @rebuild-rag="handleRebuildRag"
      />

      <TabNav
        :active-tab="activeTab"
        @change="handleTabChange"
      />

      <SolvePanel
        v-if="activeTab === 'solve'"
        v-model:question="question"
        v-model:practiceKnowledge="practiceKnowledge"
        :loading="loading"
        :image-loading="imageLoading"
        :result="result"
        :practice-loading="practiceLoading"
        :practice-list="practiceList"
        :regenerate-loading-map="regenerateLoadingMap"
        :regenerated-map="regeneratedMap"
        @submit="handleSubmit"
        @image-change="handleImageChange"
        @toggle-wrong="toggleWrong"
        @regenerate="handleRegenerateQuestion"
        @generate-practice="handleGeneratePractice"
      />

      <HistoryPanel
        v-else-if="activeTab === 'history'"
        :history-list="historyList"
        :regenerate-loading-map="regenerateLoadingMap"
        :regenerated-map="regeneratedMap"
        @toggle-wrong="toggleWrong"
        @regenerate="handleRegenerateQuestion"
      />

      <WrongPanel
        v-else-if="activeTab === 'wrong'"
        :wrong-list="wrongList"
        :regenerate-loading-map="regenerateLoadingMap"
        :regenerated-map="regeneratedMap"
        @toggle-wrong="toggleWrong"
        @regenerate="handleRegenerateQuestion"
      />

      <template v-else-if="activeTab === 'report'">
        <div v-if="reportLoading" class="empty">学习报告加载中...</div>

        <div v-else-if="learningReport" class="report-panel">
          <div class="report-summary">
            <div class="summary-card">
              <div class="summary-label">总题数</div>
              <div class="summary-value">{{ learningReport.total_count }}</div>
            </div>

            <div class="summary-card">
              <div class="summary-label">错题数</div>
              <div class="summary-value">{{ learningReport.wrong_count }}</div>
            </div>

            <div class="summary-card">
              <div class="summary-label">正确数</div>
              <div class="summary-value">{{ learningReport.correct_count }}</div>
            </div>

            <div class="summary-card">
              <div class="summary-label">错题率</div>
              <div class="summary-value">{{ learningReport.wrong_rate }}%</div>
            </div>
          </div>

          <div class="result-card">
            <h2>高频知识点 Top 5</h2>
            <div v-if="learningReport.top_knowledge_points.length === 0" class="empty">
              暂无知识点统计
            </div>
            <ul v-else class="stat-list">
              <li
                v-for="(item, index) in learningReport.top_knowledge_points"
                :key="index"
                class="stat-item"
              >
                <span>{{ item.name }}</span>
                <strong>{{ item.count }}</strong>
              </li>
            </ul>
          </div>

          <div class="result-card">
            <h2>最近练习</h2>
            <div v-if="learningReport.recent_records.length === 0" class="empty">
              暂无记录
            </div>

            <div
              v-for="item in learningReport.recent_records"
              :key="item.id"
              class="recent-item"
            >
              <div class="recent-header">
                <span>题目 #{{ item.id }}</span>
                <span :class="['status-tag', item.is_wrong ? 'wrong' : 'correct']">
                  {{ item.is_wrong ? '错题' : '正常' }}
                </span>
              </div>

              <div class="recent-question">{{ item.question }}</div>

              <div class="recent-kp">
                <span
                  v-for="(kp, idx) in item.knowledge_points"
                  :key="idx"
                  class="kp-tag"
                >
                  {{ kp }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template v-else-if="activeTab === 'graph'">
  <div v-if="graphLoading" class="empty">知识图谱加载中...</div>

  <div v-else-if="knowledgeGraph" class="report-panel">
    <div class="result-card">
      <div class="card-header">
        <h2>学生知识图谱</h2>
        <button class="retry-btn" @click="handleRebuildKnowledgeGraph">
          重建图谱
        </button>
      </div>

      <div v-if="knowledgeGraph.items.length === 0" class="empty">
        暂无知识图谱数据
      </div>

      <div v-else class="graph-list">
        <div v-for="(item, index) in knowledgeGraph.items" :key="index" class="graph-item">
          <div class="graph-header">
            <strong>{{ item.knowledge_name }}</strong>
            <span class="weak-rate">错误率 {{ item.wrong_rate }}%</span>
          </div>

          <div class="graph-meta">
            共练习 {{ item.total_count }} 次 / 正确 {{ item.correct_count }} 次 / 错误 {{ item.wrong_count }} 次
          </div>

          <div class="graph-bar">
            <div
              class="graph-bar-inner"
              :style="{ width: `${Math.min(item.wrong_rate, 100)}%` }"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<template v-else-if="activeTab === 'path'">

  <div v-if="pathLoading" class="empty">
    学习路径生成中...
  </div>

  <div v-else class="report-panel">

    <div class="result-card">

      <h2>AI学习路径</h2>

      <div
        v-for="(item,index) in learningPath"
        :key="index"
        class="path-item"
      >

        <div class="path-header">

          <strong>{{ index+1 }}. {{ item.knowledge_name }}</strong>

          <span class="weak-rate">
            错误率 {{ item.wrong_rate }}%
          </span>

        </div>

        <div class="path-suggestion">
          {{ item.suggestion }}
        </div>

      </div>

    </div>

  </div>

</template>

<PaperPanel
  v-else-if="activeTab === 'paper'"
  v-model:knowledgePoint="paperKnowledgePoint"
  v-model:count="paperCount"
  v-model:difficulty="paperDifficulty"
  v-model:preferDiagram="paperPreferDiagram"
  :loading="paperLoading"
  :paper="generatedPaper"
  @generate="handleGeneratePaper"
  @export="handleExportPaper"
/>

      <template v-else>
        <div v-if="suggestionLoading" class="empty">学习建议加载中...</div>

        <div v-else-if="studySuggestion" class="report-panel">
          <div class="result-card">
            <h2>整体学习建议</h2>
            <p>{{ studySuggestion.overall_suggestion }}</p>
          </div>

          <div class="result-card">
            <h2>薄弱知识点分析</h2>

            <div v-if="studySuggestion.weak_knowledge_points.length === 0" class="empty">
              暂无薄弱知识点
            </div>

            <div
              v-for="(item, index) in studySuggestion.weak_knowledge_points"
              :key="index"
              class="weak-item"
            >
              <div class="weak-header">
                <strong>{{ item.name }}</strong>
                <span class="weak-rate">错误率 {{ item.wrong_rate }}%</span>
              </div>

              <div class="weak-meta">
                错误 {{ item.wrong_count }} 次 / 共出现 {{ item.total_count }} 次
              </div>

              <div class="weak-suggestion">
                {{ item.suggestion }}
              </div>

              <button
                class="retry-btn"
                @click="handleGenerateWeakPractice(item.name)"
              >
                生成该知识点练习题
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import StudentBar from './components/StudentBar.vue'
import TabNav from './components/TabNav.vue'
import SolvePanel from './components/SolvePanel.vue'
import HistoryPanel from './components/HistoryPanel.vue'
import WrongPanel from './components/WrongPanel.vue'
import {
  solveMathQuestion,
  solveMathImage,
  getHistoryList,
  getWrongQuestionList,
  markWrongQuestion,
  generatePracticeByKnowledge,
  regenerateQuestion,
  getLearningReport,
  getStudySuggestion,
  getStudentList,
  createStudent,
  getExportReportUrl,
  type SolveResponse,
  type HistoryItem,
  type PracticeQuestionItem,
  type LearningReportResponse,
  type StudySuggestionResponse,
  type StudentItem,
  getKnowledgeGraph,
  rebuildKnowledgeGraph,
  type KnowledgeGraphResponse,
  rebuildRagIndex,
  getLearningPath,
  generatePaper,
  getExportPaperUrl,
  type GeneratePaperResponse,
  type LearningPathItem,
} from './api/math'
import PaperPanel from './components/PaperPanel.vue'
import { extractTextInBrowser } from './utils/browserOcr'

type AppTab =
  | 'solve'
  | 'history'
  | 'wrong'
  | 'report'
  | 'suggestion'
  | 'graph'
  | 'path'
  | 'paper'

const question = ref('')
const loading = ref(false)
const result = ref<(SolveResponse & { question: string }) | null>(null)

const activeTab = ref<AppTab>('solve')
const historyList = ref<HistoryItem[]>([])
const wrongList = ref<HistoryItem[]>([])
const imageLoading = ref(false)
const practiceKnowledge = ref('')
const practiceLoading = ref(false)
const practiceList = ref<PracticeQuestionItem[]>([])

const regenerateLoadingMap = ref<Record<number, boolean>>({})
const regeneratedMap = ref<Record<number, PracticeQuestionItem>>({})
const reportLoading = ref(false)
const learningReport = ref<LearningReportResponse | null>(null)

const studentList = ref<StudentItem[]>([])
const currentStudentId = ref(1)
const newStudentName = ref('')

const suggestionLoading = ref(false)
const studySuggestion = ref<StudySuggestionResponse | null>(null)

const graphLoading = ref(false)
const knowledgeGraph = ref<KnowledgeGraphResponse | null>(null)

const learningPath = ref<LearningPathItem[]>([])
const pathLoading = ref(false)

const paperKnowledgePoint = ref('')
const paperCount = ref(10)
const paperDifficulty = ref('中等')
const paperPreferDiagram = ref(false)
const paperLoading = ref(false)
const generatedPaper = ref<GeneratePaperResponse | null>(null)

const refreshAfterSolve = async () => {
  const refreshResults = await Promise.allSettled([
    loadHistory(),
    loadWrongList(),
  ])

  refreshResults.forEach((item) => {
    if (item.status === 'rejected') {
      console.error('刷新列表失败:', item.reason)
    }
  })

  await loadReport()
  await loadStudySuggestion()
  await loadKnowledgeGraph()
}

const applySolveResult = (data: SolveResponse, currentQuestion: string) => {
  result.value = {
    ...data,
    question: currentQuestion,
  }

  activeTab.value = 'solve'
}

const handleTabChange = async (tab: AppTab) => {
  activeTab.value = tab

  if (tab === 'history') {
    await loadHistory()
  } else if (tab === 'wrong') {
    await loadWrongList()
  } else if (tab === 'report') {
    await loadReport()
  } else if (tab === 'suggestion') {
    await loadStudySuggestion()
  } else if (tab === 'graph') {
    await loadKnowledgeGraph()
  } else if (tab === 'path') {
    await loadLearningPath()
  }
}

const handleGenerateWeakPractice = async (knowledgeName: string) => {
  practiceKnowledge.value = knowledgeName
  activeTab.value = 'solve'
  await handleGeneratePractice()
}

const loadHistory = async () => {
  const { data } = await getHistoryList(currentStudentId.value)
  historyList.value = data
}

const loadWrongList = async () => {
  const { data } = await getWrongQuestionList(currentStudentId.value)
  wrongList.value = data
}

const handleSubmit = async () => {
  if (!question.value.trim()) return

  loading.value = true
  try {
    const currentQuestion = question.value.trim()
    const { data } = await solveMathQuestion(
  { question: currentQuestion },
  currentStudentId.value
)

    console.log('solve result:', data)

    applySolveResult(data, currentQuestion)
    await refreshAfterSolve()
  } catch (error: any) {
    console.error('解析失败:', error)
    alert(error?.response?.data?.detail || '解析失败，请检查后端日志')
  } finally {
    loading.value = false
  }
}

const toggleWrong = async (item: HistoryItem | (SolveResponse & { question: string })) => {
  try {
    const { data } = await markWrongQuestion(item.id, !item.is_wrong)

    if (result.value && result.value.id === item.id) {
      result.value = {
        ...result.value,
        is_wrong: data.is_wrong,
      }
    }

    await loadHistory()
    await loadWrongList()
      await loadReport()
      await loadStudySuggestion()
    await loadKnowledgeGraph()
  } catch (error) {
    console.error(error)
    alert('更新错题状态失败')
  }
}

const handleImageChange = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  imageLoading.value = true
  try {
    const { data } = await solveMathImage(file, currentStudentId.value)
    question.value = data.question
    applySolveResult(data, data.question)
    await refreshAfterSolve()
  } catch (error: any) {
    console.error('图片解析失败，尝试浏览器 OCR 回退:', error)

    try {
      const extractedText = await extractTextInBrowser(file)
      if (!extractedText) {
        throw new Error('浏览器 OCR 未识别到题目内容')
      }

      question.value = extractedText
      const { data } = await solveMathQuestion(
        { question: extractedText },
        currentStudentId.value,
      )

      applySolveResult(data, extractedText)
      await refreshAfterSolve()
      alert('已自动切换到浏览器 OCR 识题')
    } catch (fallbackError: any) {
      console.error('浏览器 OCR 回退失败:', fallbackError)
      alert(
        fallbackError?.response?.data?.detail ||
          fallbackError?.message ||
          error?.response?.data?.detail ||
          '图片解析失败，请检查后端日志',
      )
    }
  } finally {
    imageLoading.value = false
    target.value = ''
  }
}

const handleGeneratePractice = async () => {
  if (!practiceKnowledge.value.trim()) return

  practiceLoading.value = true
  try {
    const { data } = await generatePracticeByKnowledge(practiceKnowledge.value, 3)
    practiceList.value = data.questions
  } catch (error: any) {
    console.error('生成练习题失败:', error)
    alert(error?.response?.data?.detail || '生成练习题失败')
  } finally {
    practiceLoading.value = false
  }
}

const handleRegenerateQuestion = async (id: number) => {
  regenerateLoadingMap.value[id] = true
  try {
    const { data } = await regenerateQuestion(id)
    regeneratedMap.value[id] = {
      question: data.question,
      answer: data.answer,
      steps: data.steps,
    }
  } catch (error: any) {
    console.error('再练一题失败:', error)
    alert(error?.response?.data?.detail || '再练一题失败')
  } finally {
    regenerateLoadingMap.value[id] = false
  }
}

const loadReport = async () => {
  reportLoading.value = true
  try {
    const { data } = await getLearningReport(currentStudentId.value)
    learningReport.value = data
  } catch (error: any) {
    console.error('加载学习报告失败:', error)
    alert(error?.response?.data?.detail || '加载学习报告失败')
  } finally {
    reportLoading.value = false
  }
}

const loadStudents = async () => {
  const { data } = await getStudentList()
  studentList.value = data
  const firstStudent = data[0]
  if (!data.find(item => item.id === currentStudentId.value) && firstStudent) {
    currentStudentId.value = firstStudent.id
  }
}

const handleCreateStudent = async () => {
  const name = newStudentName.value.trim()
  if (!name) return

  try {
    const { data } = await createStudent(name)
    newStudentName.value = ''
    await loadStudents()
    currentStudentId.value = data.id
    await refreshAllStudentData()
  } catch (error: any) {
    console.error('创建学生失败:', error)
    alert(error?.response?.data?.detail || '创建学生失败')
  }
}

const refreshAllStudentData = async () => {
  await Promise.all([
    loadHistory(),
    loadWrongList(),
    loadReport(),
    loadStudySuggestion(),
    loadKnowledgeGraph(),
  ])
}

const handleStudentChange = async () => {
  result.value = null
  practiceList.value = []
  regeneratedMap.value = {}
  await refreshAllStudentData()
}

const loadStudySuggestion = async () => {
  suggestionLoading.value = true
  try {
    const { data } = await getStudySuggestion(currentStudentId.value)
    studySuggestion.value = data
  } catch (error: any) {
    console.error('加载学习建议失败:', error)
    alert(error?.response?.data?.detail || '加载学习建议失败')
  } finally {
    suggestionLoading.value = false
  }
}

const handleExportReport = () => {
  const url = getExportReportUrl(currentStudentId.value)
  window.open(url, '_blank', 'noopener,noreferrer')
}

const handleRebuildRag = async () => {
  try {
    const { data } = await rebuildRagIndex()
    alert(data?.message || '知识库重建成功')
  } catch (error: any) {
    console.error('重建知识库失败:', error)
    alert(error?.response?.data?.detail || '重建知识库失败')
  }
}

const loadKnowledgeGraph = async () => {
  graphLoading.value = true
  try {
    const { data } = await getKnowledgeGraph(currentStudentId.value)
    knowledgeGraph.value = data
  } catch (error: any) {
    console.error('加载知识图谱失败:', error)
    alert(error?.response?.data?.detail || '加载知识图谱失败')
  } finally {
    graphLoading.value = false
  }
}

const handleRebuildKnowledgeGraph = async () => {
  try {
    await rebuildKnowledgeGraph(currentStudentId.value)
    await loadKnowledgeGraph()
    alert('知识图谱重建成功')
  } catch (error: any) {
    console.error('重建知识图谱失败:', error)
    alert(error?.response?.data?.detail || '重建知识图谱失败')
  }
}

const loadLearningPath = async () => {
  pathLoading.value = true
  try {
    const { data } = await getLearningPath(currentStudentId.value)
    learningPath.value = data.path
  } catch (error: any) {
    console.error(error)
  } finally {
    pathLoading.value = false
  }
}

const handleGeneratePaper = async () => {
  if (!paperKnowledgePoint.value.trim()) return

  paperLoading.value = true
  try {
    const { data } = await generatePaper(
      paperKnowledgePoint.value,
      paperCount.value,
      paperDifficulty.value,
      paperPreferDiagram.value,
    )
    generatedPaper.value = data
  } catch (error: any) {
    console.error('生成试卷失败:', error)
    alert(error?.response?.data?.detail || '生成试卷失败')
  } finally {
    paperLoading.value = false
  }
}

const handleExportPaper = async () => {
  if (!paperKnowledgePoint.value.trim()) {
    alert('请先输入知识点')
    return
  }

  const url = getExportPaperUrl()
  const form = document.createElement('form')
  form.method = 'POST'
  form.action = url
  form.target = '_blank'

  const fields = {
    knowledge_point: paperKnowledgePoint.value,
    count: String(paperCount.value),
    difficulty: paperDifficulty.value,
    prefer_diagram: String(paperPreferDiagram.value),
    paper_payload: generatedPaper.value ? JSON.stringify(generatedPaper.value) : '',
  }

  Object.entries(fields).forEach(([key, value]) => {
    const input = document.createElement('input')
    input.type = 'hidden'
    input.name = key
    input.value = value
    form.appendChild(input)
  })

  document.body.appendChild(form)
  form.submit()
  document.body.removeChild(form)
}

onMounted(async () => {
  await loadStudents()
  await refreshAllStudentData()
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top, #eef6ff 0, #f5f7fa 42%, #eef3f8 100%);
  padding: 24px 16px 40px;
}

.container {
  max-width: 960px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.96);
  padding: 24px;
  border-radius: 24px;
  box-shadow: 0 24px 60px rgba(31, 45, 61, 0.08);
  backdrop-filter: blur(12px);
}

h1 {
  margin: 0 0 8px;
  font-size: clamp(1.9rem, 3vw, 2.6rem);
  color: #162033;
}

.page :deep(h2),
.page :deep(h3),
.page :deep(h4) {
  color: #162033;
}

.page :deep(p),
.page :deep(li) {
  word-break: break-word;
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
.empty {
  padding: 32px 0;
  text-align: center;
  color: #999;
}
.report-panel {
  margin-top: 24px;
}
.report-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.summary-card {
  padding: 20px;
  background: #fafafa;
  border-radius: 12px;
  text-align: center;
}
.summary-label {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}
.summary-value {
  font-size: 28px;
  font-weight: 700;
  color: #18a058;
}
.stat-list {
  padding: 0;
  margin: 0;
  list-style: none;
}
.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}
.recent-item {
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}
.recent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.recent-question {
  margin-bottom: 10px;
  color: #333;
}
.recent-kp {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.kp-tag {
  display: inline-block;
  padding: 4px 10px;
  background: #f3f3f3;
  border-radius: 999px;
  font-size: 12px;
}
.status-tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  color: #fff;
}
.status-tag.wrong {
  background: #d03050;
}
.status-tag.correct {
  background: #18a058;
}
.weak-item {
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}
.weak-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.weak-rate {
  color: #d03050;
  font-weight: 600;
}
.weak-meta {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}
.weak-suggestion {
  margin-bottom: 12px;
  color: #333;
  line-height: 1.7;
}
.graph-list {
  margin-top: 12px;
}
.graph-item {
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}
.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.graph-meta {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}
.graph-bar {
  height: 10px;
  background: #f0f0f0;
  border-radius: 999px;
  overflow: hidden;
}

.graph-bar-inner {
  height: 100%;
  background: linear-gradient(90deg, #f0a020, #d03050);
  border-radius: 999px;
}

.path-item {
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}

.path-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.path-suggestion {
  color: #666;
  font-size: 14px;
  line-height: 1.7;
}

@media (max-width: 768px) {
  .page {
    padding: 12px 12px 28px;
  }

  .container {
    padding: 18px 14px;
    border-radius: 18px;
  }

  .report-summary {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .recent-header,
  .weak-header,
  .graph-header,
  .path-header,
  .stat-item {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 520px) {
  .report-summary {
    grid-template-columns: 1fr;
  }

  .summary-card,
  .result-card {
    padding: 16px;
  }
}
</style>
