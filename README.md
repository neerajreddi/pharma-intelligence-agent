# 💊 Agentic Pharma Intelligence System

An AI-powered multi-step agent that autonomously researches, analyzes and generates competitive pharmaceutical intelligence reports for any given disease.

## 🚀 Live Demo
Coming soon - Streamlit deployment

## 🎯 What It Does
Enter any disease name and the agent automatically:
- Searches WHO/NLEM verified drug database
- Fetches FDA approved drug data via API
- Retrieves latest PubMed research papers
- Searches real-time web for market trends
- Generates a structured business intelligence report
- Visualizes data with interactive charts

## 🛠️ Tech Stack
- **LangGraph** — Multi-step agent workflow orchestration
- **Groq API** — LLM powered analysis (llama-3.3-70b)
- **Tavily API** — Real-time web search
- **ChromaDB** — Vector database for RAG
- **SentenceTransformers** — Text embeddings
- **FDA OpenAPI** — Official drug approval data
- **PubMed API** — Clinical research papers
- **Streamlit** — Interactive web UI
- **Plotly** — Interactive data visualizations

## 📊 Report Sections Generated
- Disease Overview
- Top Drugs in Market
- Competitor Comparison
- India Market Trends
- Global Outlook
- Business Recommendations

## ⚙️ Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/neerajreddi/pharma-intelligence-agent.git
cd pharma-intelligence-agent
```

2. Create virtual environment and install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a .env file with your API keys
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

4. Setup RAG database
```bash
python rag_setup.py
```

5. Run the application
```bash
streamlit run pharma_app.py
```

## 🎯 Use Cases
- Pharmaceutical competitive intelligence
- Drug market analysis for consulting firms
- Medical research summarization
- Business development in pharma sector

## 👨‍💻 Built By
Neeraj Reddy Bayapureddy — VIT Vellore, CSE 2026
