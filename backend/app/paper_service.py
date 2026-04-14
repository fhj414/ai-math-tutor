import json
from app.llm_service import get_model_name, get_openai_client
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
6. 如果是几何题，请在题干中直接写明图形名称与关键条件，不要写“如图所示”
7. 如果是坐标系题，请在题干中直接写明点坐标、线段关系或函数关系
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


def generate_paper(
    knowledge_point: str,
    count: int = 10,
    difficulty: str = "中等",
    prefer_diagram: bool = False,
):
    client = get_openai_client()
    model_name = get_model_name()
    context = build_context(knowledge_point, top_k=3)

    user_content = (
        f"请围绕“{knowledge_point}”生成一份数学练习卷，"
        f"题量为 {count} 题，难度为“{difficulty}”。"
        "每道题都需要包含题目、答案、分步解析。"
    )

    if prefer_diagram:
        user_content += (
            " 这份试卷请优先生成适合页面绘制示意图的题目，"
            "题干中直接写出图形名称和关键尺寸、角度、坐标或对角线信息，"
            "尽量覆盖圆、三角形、四边形、坐标系等常见图形题。"
        )

    if any(keyword in knowledge_point for keyword in ["几何", "圆", "三角形", "长方形", "矩形", "正方形", "梯形", "坐标", "平行四边形"]):
        user_content += (
            " 请优先生成能够直接用文字描述图形的题目："
            "在题干中明确写出图形名称，以及边长、半径、直径、高、角度或坐标等关键条件，"
            "不要把核心信息放到“见图”里。"
        )

    if context:
        user_content += f"\n\n以下是可参考的知识库内容：\n{context}"

    resp = client.chat.completions.create(
        model=model_name,
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
