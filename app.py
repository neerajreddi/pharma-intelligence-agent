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

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Load vector database
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

class AgentState(TypedDict):
    disease: str
    pdf_results: str
    api_results: str
    web_results: str
    analysis: str
    report: str

# Step 1: Search WHO/NLEM PDF database
def search_pdf_database(state: AgentState):
    print("Step 1: Searching WHO/NLEM PDF database...")
    disease = state["disease"]
    docs = vectordb.similarity_search(disease, k=3)
    pdf_content = "\n".join([doc.page_content for doc in docs])
    return {"pdf_results": pdf_content}

# Step 2: Fetch from FDA + PubMed APIs
def search_apis(state: AgentState):
    print("Step 2: Fetching from FDA + PubMed APIs...")
    disease = state["disease"]
    api_content = fetch_all_medical_data(disease)
    return {"api_results": api_content}

# Step 3: Search web for market trends
def search_web(state: AgentState):
    print("Step 3: Searching web for market trends...")
    disease = state["disease"]
    results = tavily.search(
        query=f"{disease} drug market analysis India 2024 trends",
        max_results=5
    )
    content = "\n".join([r["content"] for r in results["results"]])
    return {"web_results": content}

# Step 4: Analyze all sources
def analyze_data(state: AgentState):
    print("Step 4: Analyzing all data sources...")
    prompt = f"""
    You are a senior pharmaceutical business analyst at a top consulting firm.
    
    Disease: {state['disease']}
    
    SOURCE 1 - WHO/NLEM Official Guidelines:
    {state['pdf_results']}
    
    SOURCE 2 - FDA Approved Drugs + PubMed Research:
    {state['api_results']}
    
    SOURCE 3 - Market Intelligence (Web):
    {state['web_results']}
    
    Using ALL THREE sources, analyze:
    1. Top 4-5 officially approved drugs for this disease
    2. Manufacturing companies and market leaders
    3. Drug effectiveness and comparison
    4. India specific market trends
    5. Global market outlook
    
    Important rules:
    - Prioritize WHO and FDA approved drugs only
    - Cross validate information across sources
    - Focus on business intelligence angle
    - Be specific with numbers and data where available
    """
    response = llm.invoke(prompt)
    return {"analysis": response.content}

# Step 5: Generate final report
def generate_report(state: AgentState):
    print("Step 5: Generating final report...")
    prompt = f"""
    Create a professional pharmaceutical business intelligence report for {state['disease']}.
    
    Based on this analysis:
    {state['analysis']}
    
    Format the report with these exact sections:
    
    DISEASE OVERVIEW
    [2-3 lines about the disease and global prevalence]
    
    TOP DRUGS IN MARKET
    [List top 4-5 drugs with company, effectiveness, approval status]
    
    COMPETITOR COMPARISON
    [Compare drugs on cost, effectiveness, market share]
    
    INDIA MARKET TRENDS
    [Specific trends, growth rates, key players in India]
    
    GLOBAL OUTLOOK
    [Global market size, CAGR, future projections]
    
    BUSINESS RECOMMENDATION
    [3-4 lines of actionable strategic insight]
    """
    response = llm.invoke(prompt)
    return {"report": response.content}

# Build workflow
workflow = StateGraph(AgentState)
workflow.add_node("pdf_search", search_pdf_database)
workflow.add_node("api_search", search_apis)
workflow.add_node("web_search", search_web)
workflow.add_node("analyze", analyze_data)
workflow.add_node("report", generate_report)

workflow.add_edge(START, "pdf_search")
workflow.add_edge("pdf_search", "api_search")
workflow.add_edge("api_search", "web_search")
workflow.add_edge("web_search", "analyze")
workflow.add_edge("analyze", "report")
workflow.add_edge("report", END)

agent = workflow.compile()

# Test
print("\nTesting agent with 'diabetes'...\n")
result = agent.invoke({"disease": "diabetes"})
print("\n===== FINAL REPORT =====")
print(result["report"])