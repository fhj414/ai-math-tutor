


# AI Math Tutor

一个基于 **Vue3 + TypeScript + FastAPI + LLM** 的 AI 数学辅导系统，面向学生、老师和家长的数学练习与学习分析场景。

## 项目简介

AI Math Tutor 旨在帮助学生更高效地完成数学练习、错题整理和知识点强化。  
系统支持题目解析、图片 OCR 识题、错题本、学习报告、学习建议、多学生切换以及练习单导出等功能。

当前项目定位为一个可持续迭代的 **AI 教育产品 MVP**，后续可继续扩展为完整的教学 SaaS 系统。

---

## 功能特性

### 1. 题目解析
- 支持手动输入数学题
- 调用大模型生成：
  - 答案
  - 分步解析
  - 知识点
  - 相似题

### 2. 图片 OCR 识题
- 支持上传数学题截图
- 使用 OCR 提取题目文字
- 自动调用 AI 进行解析

### 3. 历史记录
- 自动保存每一次解析记录
- 支持按学生维度查看历史题目

### 4. 错题本
- 支持一键加入错题本 / 取消错题
- 支持错题再练一题

### 5. 知识点练习生成
- 可按知识点生成专项练习题
- 自动返回答案与解析

### 6. 学习报告
- 总题数
- 错题数
- 正确数
- 错题率
- 高频知识点统计
- 最近练习记录

### 7. 学习建议
- 自动识别薄弱知识点
- 生成学习建议
- 一键生成对应专项练习

### 8. 多学生管理
- 支持新增学生
- 支持切换学生
- 每个学生拥有独立：
  - 历史记录
  - 错题本
  - 学习报告
  - 学习建议

### 9. 练习单导出
- 支持导出当前学生练习单
- 生成 HTML 页面
- 浏览器可直接打印 / 保存为 PDF

---

## 技术栈

### 前端
- Vue 3
- TypeScript
- Vite
- Axios

### 后端
- FastAPI
- SQLAlchemy
- SQLite

### AI / OCR
- OpenAI Compatible API / Moonshot
- PaddleOCR

---

## 项目结构

```bash
ai-math-tutor/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── llm_service.py
│   │   ├── ocr_service.py
│   │   ├── rag_service.py
│   │   ├── practice_service.py
│   │   ├── report_service.py
│   │   ├── suggestion_service.py
│   │   └── student_service.py
│   ├── data/
│   │   └── math_knowledge.json
│   ├── requirements.txt
│   └── .env
│
├── .gitignore
└── README.md
````

---

## 本地启动

## 1. 克隆项目

```bash
git clone https://github.com/你的用户名/ai-math-tutor.git
cd ai-math-tutor
```

---

## 2. 启动后端

进入后端目录：

```bash
cd backend
```

创建虚拟环境：

```bash
python3 -m venv venv
```

激活虚拟环境：

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

如果你还没有 `requirements.txt`，可以先安装：

```bash
pip install fastapi uvicorn python-dotenv openai sqlalchemy pillow paddlepaddle==2.6.2 paddleocr==2.7.3 numpy==1.26.4 opencv-python-headless==4.10.0.84
```

创建 `.env` 文件：

```env
OPENAI_API_KEY=你的key
OPENAI_BASE_URL=https://api.moonshot.cn/v1
OPENAI_MODEL=moonshot-v1-8k
```

启动后端：

```bash
uvicorn app.main:app --reload --port 8000
```

后端启动后访问：

```bash
http://127.0.0.1:8000/docs
```

---

## 3. 启动前端

进入前端目录：

```bash
cd ../frontend
```

安装依赖：

```bash
npm install
```

启动项目：

```bash
npm run dev
```

前端启动后访问：

```bash
http://127.0.0.1:5173
```

---

## 环境变量说明

后端 `.env` 配置：

```env
OPENAI_API_KEY=你的key
OPENAI_BASE_URL=https://api.moonshot.cn/v1
OPENAI_MODEL=moonshot-v1-8k
```

字段说明：

* `OPENAI_API_KEY`：大模型接口密钥
* `OPENAI_BASE_URL`：兼容 OpenAI 的模型服务地址
* `OPENAI_MODEL`：模型名称

---

## 主要页面说明

### 题目解析

支持：

* 文本输入题目
* 图片上传识题
* AI 自动解析
* 生成练习题

### 历史记录

支持：

* 查看题目历史
* 一键加入错题本
* 再练一题

### 错题本

支持：

* 管理错题
* 针对错题生成再练题

### 学习报告

展示：

* 总题数
* 错题数
* 正确数
* 错题率
* 高频知识点
* 最近练习记录

### 学习建议

分析：

* 薄弱知识点
* 错误率
* 自动建议
* 一键专项练习

---

## 当前已完成版本

* [x] 文本题目解析
* [x] OCR 图片识题
* [x] 历史记录
* [x] 错题本
* [x] 再练一题
* [x] 知识点练习生成
* [x] 学习报告
* [x] 学习建议
* [x] 多学生切换
* [x] 练习单导出
* [x] 前端组件拆分（第一轮）

---

## 后续规划

* [ ] ReportPanel / SuggestionPanel 组件拆分
* [ ] 向量数据库版 RAG
* [ ] 学习路径推荐
* [ ] 老师后台首页
* [ ] 登录态与权限系统
* [ ] Word / PDF 文件导出
* [ ] 云端部署
* [ ] 家长端查看学习报告

---

## Git 提交建议

建议按功能拆分提交，例如：

```bash
git add .
git commit -m "feat: add OCR solve support"
git commit -m "feat: add learning report panel"
git commit -m "feat: add multi-student support"
git commit -m "refactor: split app into multiple components"
```

---

## 注意事项

1. 本项目默认使用 SQLite，本地开发方便，生产环境建议切换 MySQL / PostgreSQL
2. OCR 在不同系统下安装可能存在依赖差异，建议固定版本
3. 若修改数据库模型字段，开发阶段建议删库重建或引入 Alembic 做迁移
4. 请勿将 `.env`、数据库文件、虚拟环境提交到 GitHub

---

## License

MIT

---

## 作者说明

这是一个面向 AI 教育方向的实践项目，目标是从题目解析、错题管理、学习报告逐步扩展为一个完整的 AI 学习辅助系统。


