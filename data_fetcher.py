import requests
import xmltodict
import json

# ============================================
# FDA API - Fetch approved drugs for a disease
# ============================================
def fetch_fda_drugs(disease):
    print(f"Fetching FDA approved drugs for: {disease}")
    try:
        url = "https://api.fda.gov/drug/label.json"
        params = {
            "search": f"indications_and_usage:{disease}",
            "limit": 10
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        if "results" in data:
            for drug in data["results"]:
                drug_info = {}
                
                # Get drug name
                if "openfda" in drug:
                    openfda = drug["openfda"]
                    if "brand_name" in openfda:
                        drug_info["brand_name"] = openfda["brand_name"][0]
                    if "generic_name" in openfda:
                        drug_info["generic_name"] = openfda["generic_name"][0]
                    if "manufacturer_name" in openfda:
                        drug_info["manufacturer"] = openfda["manufacturer_name"][0]
                
                # Get indications
                if "indications_and_usage" in drug:
                    drug_info["usage"] = drug["indications_and_usage"][0][:300]
                
                if drug_info:
                    results.append(drug_info)
        
        return results
    
    except Exception as e:
        print(f"FDA API error: {e}")
        return []

# ============================================
# PubMed API - Fetch latest research papers
# ============================================
def fetch_pubmed_research(disease):
    print(f"Fetching PubMed research for: {disease}")
    try:
        # Step 1: Search for paper IDs
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": f"{disease} drug treatment approved",
            "retmax": 5,
            "retmode": "json",
            "sort": "relevance"
        }
        search_response = requests.get(search_url, params=search_params, timeout=10)
        search_data = search_response.json()
        
        ids = search_data["esearchresult"]["idlist"]
        
        if not ids:
            return []
        
        # Step 2: Fetch paper details
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml",
            "rettype": "abstract"
        }
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=10)
        data = xmltodict.parse(fetch_response.text)
        
        results = []
        articles = data.get("PubmedArticleSet", {}).get("PubmedArticle", [])
        
        if isinstance(articles, dict):
            articles = [articles]
        
        for article in articles[:5]:
            try:
                paper = {}
                medline = article["MedlineCitation"]
                article_data = medline["Article"]
                
                paper["title"] = article_data.get("ArticleTitle", "")
                
                abstract = article_data.get("Abstract", {})
                if abstract:
                    abstract_text = abstract.get("AbstractText", "")
                    if isinstance(abstract_text, list):
                        paper["abstract"] = " ".join([str(a) for a in abstract_text])[:400]
                    else:
                        paper["abstract"] = str(abstract_text)[:400]
                
                results.append(paper)
            except:
                continue
        
        return results
    
    except Exception as e:
        print(f"PubMed API error: {e}")
        return []

# ============================================
# Combine both sources
# ============================================
def fetch_all_medical_data(disease):
    print(f"\nFetching all medical data for: {disease}")
    print("=" * 50)
    
    fda_data = fetch_fda_drugs(disease)
    pubmed_data = fetch_pubmed_research(disease)
    
    # Format FDA data as text
    fda_text = "FDA APPROVED DRUGS:\n"
    for drug in fda_data:
        fda_text += f"- Brand: {drug.get('brand_name', 'N/A')}\n"
        fda_text += f"  Generic: {drug.get('generic_name', 'N/A')}\n"
        fda_text += f"  Manufacturer: {drug.get('manufacturer', 'N/A')}\n"
        fda_text += f"  Usage: {drug.get('usage', 'N/A')[:200]}\n\n"
    
    # Format PubMed data as text
    pubmed_text = "LATEST MEDICAL RESEARCH:\n"
    for paper in pubmed_data:
        pubmed_text += f"- Title: {paper.get('title', 'N/A')}\n"
        pubmed_text += f"  Summary: {paper.get('abstract', 'N/A')}\n\n"
    
    combined = fda_text + "\n" + pubmed_text
    return combined

# Test it
if __name__ == "__main__":
    result = fetch_all_medical_data("diabetes")
    print(result)