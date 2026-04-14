import json
from app.llm_service import get_model_name, get_openai_client
from app.rag_service import build_context


PRACTICE_SYSTEM_PROMPT = """
你是一位专业的初中数学老师。

请严格返回 JSON，不要返回 markdown，不要加 ```json。

如果题目涉及几何图形，请优先生成便于页面渲染示意图的题目表达：
1. 在 question 中直接写明图形名称，例如圆、扇形、长方形、正方形、三角形、梯形、坐标系。
2. 在 question 中直接写明关键尺寸或条件，例如半径 4 厘米、底 6 高 4、直角边长分别为 3 和 4。
3. 不要依赖“如图所示”“见下图”这类页面外图片描述，题干本身必须完整。
4. 如果是坐标系题，请在 question 中明确点的坐标或函数关系。

如果用户要求生成练习题，请返回：
{
  "knowledge_point": "知识点名称",
  "questions": [
    {
      "question": "题目1",
      "answer": "答案1",
      "steps": ["步骤1", "步骤2"]
    }
  ]
}

如果用户要求基于某道题生成再练一题，请返回：
{
  "question": "新的相似题",
  "answer": "对应答案",
  "steps": ["步骤1", "步骤2"]
}
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


def generate_practice_by_knowledge(knowledge_point: str, count: int = 3):
    client = get_openai_client()
    model_name = get_model_name()
    context = build_context(knowledge_point)

    user_content = (
        f"请围绕知识点“{knowledge_point}”生成 {count} 道适合初中学生的练习题，"
        "每道题都要包含题目、答案、分步解析。"
    )

    if any(keyword in knowledge_point for keyword in ["几何", "圆", "三角形", "长方形", "矩形", "正方形", "梯形", "坐标", "平行四边形"]):
        user_content += (
            " 这些题请优先生成为带明确图形信息的题目："
            "题干中直接写出图形名称、边长、半径、直径、高、角度或坐标，"
            "避免使用“如图所示”。"
        )

    if context:
        user_content += f"\n\n可参考知识库内容：\n{context}"

    resp = client.chat.completions.create(
        model=model_name,
        temperature=0.5,
        messages=[
            {"role": "system", "content": PRACTICE_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )

    content = _clean_json_text(resp.choices[0].message.content or "")
    data = json.loads(content)

    if "knowledge_point" not in data or "questions" not in data:
        raise ValueError(f"练习题返回格式错误：{data}")

    if not isinstance(data["questions"], list):
        raise ValueError(f"questions 不是数组：{data}")

    return data


def regenerate_similar_question(source_question: str):
    client = get_openai_client()
    model_name = get_model_name()
    context = build_context(source_question)

    user_content = (
        f"基于下面这道题，生成 1 道同类型、同难度、但数字不同的新题，并给出答案和分步解析：\n"
        f"{source_question}"
    )

    if any(keyword in source_question for keyword in ["圆", "扇形", "三角形", "长方形", "矩形", "正方形", "梯形", "坐标", "平行四边形"]):
        user_content += (
            "\n请保留原题的图形类型，并在新题题干中明确写出图形名称和关键尺寸或坐标，"
            "不要使用“如图所示”。"
        )

    if context:
        user_content += f"\n\n可参考知识库内容：\n{context}"

    resp = client.chat.completions.create(
        model=model_name,
        temperature=0.5,
        messages=[
            {"role": "system", "content": PRACTICE_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )

    content = _clean_json_text(resp.choices[0].message.content or "")
    data = json.loads(content)

    for key in ["question", "answer", "steps"]:
        if key not in data:
            raise ValueError(f"再练题返回格式错误，缺少 {key}：{data}")

    if not isinstance(data["steps"], list):
        raise ValueError(f"steps 不是数组：{data}")

    return data
