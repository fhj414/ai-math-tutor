import axios from "axios";

const request = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 30000,
});

export interface SolveRequest {
  question: string;
}

export interface HistoryItem {
  id: number;
  question: string;
  answer: string;
  steps: string[];
  knowledge_points: string[];
  similar_question: string;
  is_wrong: boolean;
}

export type SolveResponse = HistoryItem;

export function solveMathQuestion(data: SolveRequest, student_id: number) {
  return request.post<SolveResponse>("/api/solve", data, {
    params: { student_id },
  });
}

export function getHistoryList(student_id: number) {
  return request.get<HistoryItem[]>("/api/history", {
    params: { student_id },
  });
}

export function getWrongQuestionList(student_id: number) {
  return request.get<HistoryItem[]>("/api/wrong-questions", {
    params: { student_id },
  });
}

export function markWrongQuestion(id: number, is_wrong: boolean) {
  return request.patch<HistoryItem>(`/api/history/${id}/wrong`, { is_wrong });
}

export interface OCRSolveResponse extends HistoryItem {
  question: string;
  ocr_text: string;
}

export function solveMathImage(file: File, student_id: number) {
  const formData = new FormData();
  formData.append("file", file);
  return request.post<OCRSolveResponse>("/api/solve-image", formData, {
    params: { student_id },
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export interface PracticeQuestionItem {
  question: string;
  answer: string;
  steps: string[];
}

export interface GeneratePracticeResponse {
  knowledge_point: string;
  questions: PracticeQuestionItem[];
}

export interface RegenerateQuestionResponse {
  source_question_id: number;
  question: string;
  answer: string;
  steps: string[];
}

export function generatePracticeByKnowledge(
  knowledge_point: string,
  count = 3,
) {
  return request.post<GeneratePracticeResponse>("/api/generate-practice", {
    knowledge_point,
    count,
  });
}

export function regenerateQuestion(id: number) {
  return request.post<RegenerateQuestionResponse>(
    `/api/history/${id}/regenerate`,
  );
}

export interface KnowledgeStatItem {
  name: string;
  count: number;
}

export interface RecentRecordItem {
  id: number;
  question: string;
  is_wrong: boolean;
  knowledge_points: string[];
}

export interface LearningReportResponse {
  total_count: number;
  wrong_count: number;
  correct_count: number;
  wrong_rate: number;
  top_knowledge_points: KnowledgeStatItem[];
  recent_records: RecentRecordItem[];
}

export function getLearningReport(student_id: number) {
  return request.get<LearningReportResponse>("/api/report", {
    params: { student_id },
  });
}

export interface WeakKnowledgeItem {
  name: string;
  wrong_count: number;
  total_count: number;
  wrong_rate: number;
  suggestion: string;
}

export interface StudySuggestionResponse {
  weak_knowledge_points: WeakKnowledgeItem[];
  overall_suggestion: string;
}

export function getStudySuggestion(student_id: number) {
  return request.get<StudySuggestionResponse>("/api/study-suggestion", {
    params: { student_id },
  });
}

export interface StudentItem {
  id: number;
  name: string;
}

export function getStudentList() {
  return request.get<StudentItem[]>("/api/students");
}

export function createStudent(name: string) {
  return request.post<StudentItem>("/api/students", { name });
}

export function getExportReportUrl(student_id: number) {
  return `http://127.0.0.1:8000/api/export/report?student_id=${student_id}`;
}

export function rebuildRagIndex() {
  return request.post("/api/rag/rebuild");
}

export interface KnowledgeGraphItem {
  knowledge_name: string;
  total_count: number;
  wrong_count: number;
  correct_count: number;
  wrong_rate: number;
}

export interface KnowledgeGraphResponse {
  student_id: number;
  items: KnowledgeGraphItem[];
}

export function getKnowledgeGraph(student_id: number) {
  return request.get<KnowledgeGraphResponse>("/api/knowledge-graph", {
    params: { student_id },
  });
}

export function rebuildKnowledgeGraph(student_id: number) {
  return request.post("/api/knowledge-graph/rebuild", null, {
    params: { student_id },
  });
}

export interface LearningPathItem {
  knowledge_name: string;
  wrong_rate: number;
  suggestion: string;
}

export function getLearningPath(student_id: number) {
  return request.get("/api/learning-path", {
    params: { student_id },
  });
}

export interface PaperQuestionItem {
  question: string;
  answer: string;
  steps: string[];
}

export interface GeneratePaperResponse {
  knowledge_point: string;
  difficulty: string;
  questions: PaperQuestionItem[];
}

export function generatePaper(
  knowledge_point: string,
  count = 10,
  difficulty = "中等",
) {
  return request.post<GeneratePaperResponse>("/api/generate-paper", {
    knowledge_point,
    count,
    difficulty,
  });
}

export function getExportPaperUrl() {
  return "http://127.0.0.1:8000/api/export/paper";
}
