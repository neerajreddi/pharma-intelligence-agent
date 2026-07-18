# 💊 Agentic Pharma Intelligence System

> **An AI-powered multi-agent pharmaceutical intelligence platform built using LangGraph, Retrieval-Augmented Generation (RAG), FDA API, PubMed API, WHO/NLEM knowledge base, and Streamlit.**

This project automates pharmaceutical research by collecting information from trusted medical sources, analyzing it using Large Language Models (LLMs), and generating structured competitive intelligence reports for any disease.

---

# 🚀 Project Highlights

- 🤖 Built an autonomous multi-agent workflow using **LangGraph**
- 📚 Integrated Retrieval-Augmented Generation (RAG) using WHO/NLEM medical documents
- 💊 Retrieved FDA-approved drug information using the FDA Open API
- 📖 Fetched latest clinical research papers from PubMed
- 🌐 Performed real-time pharmaceutical market research using Tavily Search
- 📊 Generated structured business intelligence reports with AI
- 📈 Visualized insights using interactive Plotly dashboards

---

# 🏗️ System Architecture

```text
                    User
                      │
                      ▼
              Streamlit Web App
                      │
                      ▼
              LangGraph AI Agent
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 WHO/NLEM RAG     FDA API         PubMed API
      │               │                │
      └───────────────┼────────────────┘
                      ▼
              Tavily Web Search
                      ▼
            LLM (Groq - Llama 3.3 70B)
                      ▼
      Structured Pharmaceutical Report
                      ▼
             Plotly Visualizations
```

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| AI Agent Framework | LangGraph |
| Large Language Model | Groq (Llama 3.3 70B) |
| Vector Database | ChromaDB |
| Embedding Model | Sentence Transformers |
| Retrieval System | WHO/NLEM RAG Database |
| APIs | FDA Open API, PubMed API |
| Web Search | Tavily API |
| Frontend | Streamlit |
| Visualization | Plotly |

---

# 🎯 What the Agent Does

Given any disease name, the AI agent automatically:

- Searches the WHO/NLEM drug database
- Retrieves FDA-approved medications
- Fetches the latest PubMed research papers
- Performs real-time pharmaceutical market analysis
- Compares competitor drugs
- Summarizes India and global market trends
- Generates business recommendations
- Produces an AI-powered pharmaceutical intelligence report

---

# 📊 Generated Report Includes

- Disease Overview
- Top Drugs in the Market
- FDA Approved Medicines
- Competitor Drug Comparison
- Latest Research Publications
- India Market Trends
- Global Market Outlook
- Business Recommendations

---

# 📌 Project Status

- ✅ Core AI Agent Completed
- ✅ LangGraph Workflow Implemented
- ✅ WHO/NLEM RAG Integration
- ✅ FDA API Integration
- ✅ PubMed API Integration
- ✅ Tavily Web Search Integration
- ✅ Interactive Plotly Visualizations
- 🚧 Deployment and UI enhancements are currently in progress

---

# 📂 Project Structure

```text
pharma-intelligence-agent/
│
├── medical_docs/
├── chroma_db/
├── app.py
├── rag_setup.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/neerajreddi/pharma-intelligence-agent.git

cd pharma-intelligence-agent
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY

TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

## Build the Vector Database

```bash
python rag_setup.py
```

---

## Run the Application

```bash
streamlit run app.py
```

---

# 🔄 Workflow

```text
User enters disease name

↓

WHO/NLEM Knowledge Retrieval

↓

FDA Drug Information

↓

PubMed Research Retrieval

↓

Real-time Market Search

↓

LLM Analysis

↓

Competitive Intelligence Report

↓

Interactive Dashboard
```

---

# 💡 Use Cases

- Pharmaceutical Competitive Intelligence
- Drug Market Analysis
- Healthcare Consulting
- Medical Research Summarization
- Clinical Decision Support
- Pharmaceutical Business Strategy

---

# 🚀 Future Improvements

- PDF Report Export
- Clinical Trial Integration
- Drug Interaction Analysis
- Multi-language Support
- User Authentication
- Docker Support
- AWS Cloud Deployment

---

# 👨‍💻 Author

**Neeraj Kumar Reddy Bayapureddy**

🎓 B.Tech Computer Science & Engineering  
**Vellore Institute of Technology (VIT)**

💼 Machine Learning Intern @ Waterlabs.AI

📧 Email: **iamneerajreddi@gmail.com**

💼 LinkedIn: **https://www.linkedin.com/in/neerajreddi**

💻 GitHub: **https://github.com/neerajreddi**

---

# 📄 License

This project is licensed under the **MIT License**.

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!
