from pydantic import BaseModel
from typing import List


class SolveQuestionRequest(BaseModel):
    question: str


class SolveQuestionResponse(BaseModel):
    id: int
    answer: str
    steps: List[str]
    knowledge_points: List[str]
    similar_question: str
    is_wrong: bool


class HistoryItem(BaseModel):
    id: int
    question: str
    answer: str
    steps: List[str]
    knowledge_points: List[str]
    similar_question: str
    is_wrong: bool

    class Config:
        from_attributes = True


class MarkWrongRequest(BaseModel):
    is_wrong: bool

class OCRSolveResponse(SolveQuestionResponse):
    question: str
    ocr_text: str

class PracticeQuestionItem(BaseModel):
    question: str
    answer: str
    steps: List[str]


class GeneratePracticeRequest(BaseModel):
    knowledge_point: str
    count: int = 3


class GeneratePracticeResponse(BaseModel):
    knowledge_point: str
    questions: List[PracticeQuestionItem]


class RegenerateQuestionResponse(BaseModel):
    source_question_id: int
    question: str
    answer: str
    steps: List[str]

class KnowledgeStatItem(BaseModel):
    name: str
    count: int


class RecentRecordItem(BaseModel):
    id: int
    question: str
    is_wrong: bool
    knowledge_points: List[str]


class LearningReportResponse(BaseModel):
    total_count: int
    wrong_count: int
    correct_count: int
    wrong_rate: float
    top_knowledge_points: List[KnowledgeStatItem]
    recent_records: List[RecentRecordItem]

class WeakKnowledgeItem(BaseModel):
    name: str
    wrong_count: int
    total_count: int
    wrong_rate: float
    suggestion: str


class StudySuggestionResponse(BaseModel):
    weak_knowledge_points: List[WeakKnowledgeItem]
    overall_suggestion: str

class StudentItem(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CreateStudentRequest(BaseModel):
    name: str

class KnowledgeGraphItem(BaseModel):
    knowledge_name: str
    total_count: int
    wrong_count: int
    correct_count: int
    wrong_rate: float


class KnowledgeGraphResponse(BaseModel):
    student_id: int
    items: List[KnowledgeGraphItem]

class PaperQuestionItem(BaseModel):
    question: str
    answer: str
    steps: List[str]


class GeneratePaperRequest(BaseModel):
    knowledge_point: str
    count: int = 10
    difficulty: str = "中等"


class GeneratePaperResponse(BaseModel):
    knowledge_point: str
    difficulty: str
    questions: List[PaperQuestionItem]