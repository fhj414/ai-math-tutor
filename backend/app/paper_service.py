import json
from app.llm_service import client, MODEL
from app.rag_service import build_context


PAPER_SYSTEM_PROMPT = """
你是一位专业的初中数学老师。

请严格返回 JSON，不要返回 markdown，不要加 ```json。

格式如下：
{
  "knowledge_point": "知识点名称",
  "difficulty": "难度",
  "questions": [
    {
      "question": "题目1",
      "answer": "答案1",
      "steps": ["步骤1", "步骤2"]
    }
  ]
}

要求：
1. questions 必须是数组
2. 每道题都要有 question、answer、steps
3. steps 必须适合初中学生理解
4. 题目难度要和用户要求一致
5. 不要输出 JSON 以外的内容
"""


def _clean_json_text(content: str) -> str:
    content = (content or "").strip()

    if content.startswith("```json"):
        content = content.removeprefix("```json").strip()
    if content.startswith("```"):
        content = content.removeprefix("```").strip()
    if content.endswith("```"):
        content = content.removesuffix("```").strip()

    return content


def generate_paper(knowledge_point: str, count: int = 10, difficulty: str = "中等"):
    context = build_context(knowledge_point, top_k=3)

    user_content = (
        f"请围绕“{knowledge_point}”生成一份数学练习卷，"
        f"题量为 {count} 题，难度为“{difficulty}”。"
        "每道题都需要包含题目、答案、分步解析。"
    )

    if context:
        user_content += f"\n\n以下是可参考的知识库内容：\n{context}"

    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0.5,
        messages=[
            {"role": "system", "content": PAPER_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )

    content = _clean_json_text(resp.choices[0].message.content or "")
    data = json.loads(content)

    if "knowledge_point" not in data or "difficulty" not in data or "questions" not in data:
        raise ValueError(f"试卷返回格式错误：{data}")

    if not isinstance(data["questions"], list):
        raise ValueError(f"questions 不是数组：{data}")

    return data