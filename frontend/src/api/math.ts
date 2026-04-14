import axios from "axios";

function normalizeApiBase(rawBase?: string) {
  const fallbackBase = "/api";
  const base = (rawBase || fallbackBase).trim();

  if (!base) return fallbackBase;
  if (base.startsWith("/")) return base.replace(/\/+$/, "") || fallbackBase;

  try {
    const url = new URL(base);
    const normalizedPath = url.pathname.replace(/\/+$/, "");
    if (!normalizedPath || normalizedPath === "/") {
      url.pathname = "/api";
    }
    return url.toString().replace(/\/+$/, "");
  } catch {
    return base.replace(/\/+$/, "");
  }
}

const normalizedApiBase = normalizeApiBase(
  import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_BASE,
);

const request = axios.create({
  baseURL: normalizedApiBase,
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
  return request.post<SolveResponse>("/solve", data, {
    params: { student_id },
  });
}

export function getHistoryList(student_id: number) {
  return request.get<HistoryItem[]>("/history", {
    params: { student_id },
  });
}

export function getWrongQuestionList(student_id: number) {
  return request.get<HistoryItem[]>("/wrong-questions", {
    params: { student_id },
  });
}

export function markWrongQuestion(id: number, is_wrong: boolean) {
  return request.patch<HistoryItem>(`/history/${id}/wrong`, { is_wrong });
}

export interface OCRSolveResponse extends HistoryItem {
  question: string;
  ocr_text: string;
}

export function solveMathImage(file: File, student_id: number) {
  const formData = new FormData();
  formData.append("file", file);
  return request.post<OCRSolveResponse>("/solve-image", formData, {
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
  return request.post<GeneratePracticeResponse>("/generate-practice", {
    knowledge_point,
    count,
  });
}

export function regenerateQuestion(id: number) {
  return request.post<RegenerateQuestionResponse>(
    `/history/${id}/regenerate`,
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
  return request.get<LearningReportResponse>("/report", {
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
  return request.get<StudySuggestionResponse>("/study-suggestion", {
    params: { student_id },
  });
}

export interface StudentItem {
  id: number;
  name: string;
}

export function getStudentList() {
  return request.get<StudentItem[]>("/students");
}

export function createStudent(name: string) {
  return request.post<StudentItem>("/students", { name });
}

export function getExportReportUrl(student_id: number) {
  return `${normalizedApiBase}/export/report?student_id=${student_id}`;
}

export function rebuildRagIndex() {
  return request.post("/rag/rebuild");
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
  return request.get<KnowledgeGraphResponse>("/knowledge-graph", {
    params: { student_id },
  });
}

export function rebuildKnowledgeGraph(student_id: number) {
  return request.post("/knowledge-graph/rebuild", null, {
    params: { student_id },
  });
}

export interface LearningPathItem {
  knowledge_name: string;
  wrong_rate: number;
  suggestion: string;
}

export function getLearningPath(student_id: number) {
  return request.get<{ student_id: number; path: LearningPathItem[] }>(
    "/learning-path",
    {
      params: { student_id },
    },
  );
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
  prefer_diagram = false,
) {
  return request.post<GeneratePaperResponse>("/generate-paper", {
    knowledge_point,
    count,
    difficulty,
    prefer_diagram,
  });
}

export function getExportPaperUrl() {
  return `${normalizedApiBase}/export/paper`;
}
