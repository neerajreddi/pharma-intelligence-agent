import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langgraph.graph import StateGraph, END, START
from typing import TypedDict
from data_fetcher import fetch_all_medical_data

load_dotenv()

st.set_page_config(
    page_title="Pharma Intelligence Agent",
    page_icon="💊",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1F4E79;
        text-align: center;
        padding: 20px 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #444444;
        text-align: center;
        margin-bottom: 30px;
    }
    .step-box {
        background-color: #EBF5FB;
        border-left: 4px solid #1F4E79;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 4px;
        font-size: 0.95rem;
    }
    .report-box {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        border-radius: 8px;
        padding: 25px;
        margin-top: 20px;
    }
    .source-badge {
        background-color: #1F4E79;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile"
    )
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return llm, tavily, vectordb

llm, tavily, vectordb = load_models()

class AgentState(TypedDict):
    disease: str
    pdf_results: str
    api_results: str
    web_results: str
    analysis: str
    report: str
    chart_data: dict

def search_pdf_database(state: AgentState):
    docs = vectordb.similarity_search(state["disease"], k=3)
    pdf_content = "\n".join([doc.page_content for doc in docs])
    return {"pdf_results": pdf_content}

def search_apis(state: AgentState):
    api_content = fetch_all_medical_data(state["disease"])
    return {"api_results": api_content}

def search_web(state: AgentState):
    results = tavily.search(
        query=f"{state['disease']} drug market analysis India 2024 trends",
        max_results=5
    )
    content = "\n".join([r["content"] for r in results["results"]])
    return {"web_results": content}

def analyze_data(state: AgentState):
    prompt = f"""
    You are a senior pharmaceutical business analyst.
    Disease: {state['disease']}
    
    SOURCE 1 - WHO/NLEM Guidelines: {state['pdf_results']}
    SOURCE 2 - FDA + PubMed Data: {state['api_results']}
    SOURCE 3 - Market Intelligence: {state['web_results']}
    
    Analyze top approved drugs, companies, market trends and India insights.
    Only include WHO/FDA approved drugs.
    """
    response = llm.invoke(prompt)
    return {"analysis": response.content}

def generate_report(state: AgentState):
    prompt = f"""
    Create a professional pharmaceutical business intelligence report for {state['disease']}.
    
    Based on: {state['analysis']}
    
    Use these exact sections:
    
    DISEASE OVERVIEW
    [2-3 lines about disease and global prevalence]
    
    TOP DRUGS IN MARKET
    [Top 4-5 drugs with company and approval status]
    
    COMPETITOR COMPARISON
    [Compare drugs on cost, effectiveness, market share]
    
    INDIA MARKET TRENDS
    [Specific India trends, growth rates, key players]
    
    GLOBAL OUTLOOK
    [Global market size, CAGR, projections]
    
    BUSINESS RECOMMENDATION
    [3-4 lines of strategic insight]
    """
    response = llm.invoke(prompt)
    return {"report": response.content}

def generate_chart_data(state: AgentState):
    prompt = f"""
    Based on this pharmaceutical analysis for {state['disease']}:
    {state['analysis']}
    
    Return ONLY a Python dictionary with exactly this structure, no extra text:
    {{
        "drugs": ["Drug1", "Drug2", "Drug3", "Drug4", "Drug5"],
        "market_share": [35, 25, 20, 12, 8],
        "years": [2020, 2021, 2022, 2023, 2024, 2025, 2026],
        "growth": [100, 108, 118, 130, 144, 160, 178],
        "categories": ["Branded", "Generic", "Biosimilar", "OTC"],
        "category_values": [40, 35, 15, 10]
    }}
    
    Replace Drug1-5 with actual drug names for {state['disease']}.
    Keep numbers realistic for the disease market.
    Return ONLY the dictionary, nothing else.
    """
    response = llm.invoke(prompt)
    try:
        import ast
        text = response.content.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("python"):
                text = text[6:]
        chart_data = ast.literal_eval(text.strip())
    except:
        chart_data = {
            "drugs": ["Drug A", "Drug B", "Drug C", "Drug D", "Drug E"],
            "market_share": [35, 25, 20, 12, 8],
            "years": [2020, 2021, 2022, 2023, 2024, 2025, 2026],
            "growth": [100, 108, 118, 130, 144, 160, 178],
            "categories": ["Branded", "Generic", "Biosimilar", "OTC"],
            "category_values": [40, 35, 15, 10]
        }
    return {"chart_data": chart_data}

@st.cache_resource
def build_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("pdf_search", search_pdf_database)
    workflow.add_node("api_search", search_apis)
    workflow.add_node("web_search", search_web)
    workflow.add_node("analyze", analyze_data)
    workflow.add_node("report", generate_report)
    workflow.add_node("charts", generate_chart_data)

    workflow.add_edge(START, "pdf_search")
    workflow.add_edge("pdf_search", "api_search")
    workflow.add_edge("api_search", "web_search")
    workflow.add_edge("web_search", "analyze")
    workflow.add_edge("analyze", "report")
    workflow.add_edge("report", "charts")
    workflow.add_edge("charts", END)

    return workflow.compile()

agent = build_agent()

# =============================
# UI Layout
# =============================
st.markdown('<div class="main-header">💊 Pharma Intelligence Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered competitive drug analysis using WHO, FDA, PubMed & Real-time Web Data</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom:30px;">
    <span class="source-badge">📄 WHO/NLEM Database</span>
    <span class="source-badge">💊 FDA API</span>
    <span class="source-badge">🔬 PubMed Research</span>
    <span class="source-badge">🌐 Live Web Search</span>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    disease_input = st.text_input(
        "🔍 Enter Disease Name",
        placeholder="e.g. diabetes, hypertension, cancer...",
        help="Enter any disease to generate a comprehensive pharma intelligence report"
    )
    analyze_button = st.button("🚀 Generate Intelligence Report", use_container_width=True)

if analyze_button and disease_input:
    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 🤖 Agent Progress")
        step1 = st.empty()
        step2 = st.empty()
        step3 = st.empty()
        step4 = st.empty()
        step5 = st.empty()
        step6 = st.empty()

        step1.markdown('<div class="step-box">⏳ Step 1: Searching WHO/NLEM Database...</div>', unsafe_allow_html=True)
        step2.markdown('<div class="step-box">⌛ Step 2: Fetching FDA + PubMed APIs...</div>', unsafe_allow_html=True)
        step3.markdown('<div class="step-box">⌛ Step 3: Searching Web for Market Trends...</div>', unsafe_allow_html=True)
        step4.markdown('<div class="step-box">⌛ Step 4: Analyzing All Sources...</div>', unsafe_allow_html=True)
        step5.markdown('<div class="step-box">⌛ Step 5: Generating Report...</div>', unsafe_allow_html=True)
        step6.markdown('<div class="step-box">⌛ Step 6: Building Visual Charts...</div>', unsafe_allow_html=True)

    with col2:
        with st.spinner(f"Generating intelligence report for **{disease_input}**..."):
            try:
                pdf_result = search_pdf_database({"disease": disease_input})
                step1.markdown('<div class="step-box">✅ Step 1: WHO/NLEM Database Searched!</div>', unsafe_allow_html=True)

                api_result = search_apis({"disease": disease_input})
                step2.markdown('<div class="step-box">✅ Step 2: FDA + PubMed Data Fetched!</div>', unsafe_allow_html=True)

                web_result = search_web({"disease": disease_input})
                step3.markdown('<div class="step-box">✅ Step 3: Web Market Data Retrieved!</div>', unsafe_allow_html=True)

                combined_state = {
                    "disease": disease_input,
                    "pdf_results": pdf_result["pdf_results"],
                    "api_results": api_result["api_results"],
                    "web_results": web_result["web_results"]
                }
                analysis_result = analyze_data(combined_state)
                step4.markdown('<div class="step-box">✅ Step 4: Data Analysis Complete!</div>', unsafe_allow_html=True)

                combined_state["analysis"] = analysis_result["analysis"]
                report_result = generate_report(combined_state)
                step5.markdown('<div class="step-box">✅ Step 5: Report Generated!</div>', unsafe_allow_html=True)

                chart_result = generate_chart_data(combined_state)
                step6.markdown('<div class="step-box">✅ Step 6: Visual Charts Ready!</div>', unsafe_allow_html=True)

                # Display Report
                st.success("✅ Intelligence Report Ready!")
                st.markdown('<div class="report-box">', unsafe_allow_html=True)
                st.markdown(f"## 📊 Pharma Intelligence Report: {disease_input.title()}")
                st.markdown(report_result["report"])
                st.markdown('</div>', unsafe_allow_html=True)

                # =============================
                # CHARTS SECTION
                # =============================
                st.markdown("---")
                st.markdown("## 📈 Visual Market Analytics")

                chart_data = chart_result["chart_data"]
                c1, c2, c3 = st.columns(3)

                with c1:
                    fig1 = px.bar(
                        x=chart_data["drugs"],
                        y=chart_data["market_share"],
                        title=f"Top Drugs Market Share (%) — {disease_input.title()}",
                        color=chart_data["market_share"],
                        color_continuous_scale="Blues",
                        labels={"x": "Drug", "y": "Market Share (%)"}
                    )
                    fig1.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        showlegend=False
                    )
                    st.plotly_chart(fig1, use_container_width=True)

                with c2:
                    fig2 = px.line(
                        x=chart_data["years"],
                        y=chart_data["growth"],
                        title=f"India Market Growth Index — {disease_input.title()}",
                        markers=True,
                        labels={"x": "Year", "y": "Market Index"}
                    )
                    fig2.update_traces(line_color="#1F4E79", line_width=3)
                    fig2.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig2, use_container_width=True)

                with c3:
                    fig3 = px.pie(
                        names=chart_data["categories"],
                        values=chart_data["category_values"],
                        title=f"Drug Category Distribution — {disease_input.title()}",
                        color_discrete_sequence=px.colors.sequential.Blues_r
                    )
                    fig3.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(fig3, use_container_width=True)

                # Download button
                st.download_button(
                    label="📥 Download Report",
                    data=report_result["report"],
                    file_name=f"{disease_input}_pharma_report.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error generating report: {str(e)}")

elif analyze_button and not disease_input:
    st.warning("⚠️ Please enter a disease name first!")

st.divider()
st.markdown("""
<div style="text-align:center; color:#888; font-size:0.85rem;">
    Built with LangGraph • Groq • Tavily • ChromaDB • Streamlit
</div>
""", unsafe_allow_html=True)