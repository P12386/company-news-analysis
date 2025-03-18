
from fastapi import FastAPI
from news_scraper import get_news_articles
from sentiment_analysis import analyze_sentiments
from tts import generate_tts

app = FastAPI()

@app.get("/")
def get_news_articles(company: str):
    # Your function logic here

    return {"message":"FastAPI is running successfully!"}

@app.get("/analyze/{company}")
def analyze_company(company: str):
    # Step 1: Extract news articles
    articles = get_news_articles(company)
    
    if not articles:
        return {"error": "No articles found for the company."}

    # Step 2: Perform sentiment analysis
    analyzed_articles, sentiment_distribution = analyze_sentiments(articles)

    # Step 3: Convert summarized content to Hindi TTS
    audio_file = generate_tts(analyzed_articles)

    # Step 4: Return structured response
    return {
        "Company": company,
        "Articles": analyzed_articles,
        "Comparative Sentiment Score": sentiment_distribution,
        "Audio": audio_file  # Path to generated Hindi audio file
    }

