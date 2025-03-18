import gradio as gr
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS
import os

# Function to scrape Bing News
def fetch_news(company_name):
    search_url = f"https://www.bing.com/news/search?q={company_name}&FORM=HDRSC6"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return ["Error fetching news. Try again."]

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract news headlines
    headlines = soup.select("a.title")  # Adjusted for Bing News

    if not headlines:
        return ["No relevant news found."]

    news_list = [headline.get_text() for headline in headlines[:3]]
    return news_list

# Load sentiment analysis model
sentiment_pipeline = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")

# Function to analyze news sentiment
def analyze_news(company_name):
    news_list = fetch_news(company_name)

    if not news_list or news_list == ["No relevant news found."]:
        return "No news found.", None

    # Perform sentiment analysis
    sentiment_results = [sentiment_pipeline(article)[0] for article in news_list]

    # Map labels to user-friendly sentiment names
    sentiment_mapping = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}

    # Prepare result summary
    analysis_result = "\n".join(
        [f"{i+1}. {article} - Sentiment: {sentiment_mapping[result['label']]} (Score: {result['score']:.2f})" 
         for i, (article, result) in enumerate(zip(news_list, sentiment_results))]
    )

    # Generate Hindi TTS
    try:
        tts = gTTS(text=analysis_result, lang="hi")
        tts_path = "news_analysis.mp3"
        tts.save(tts_path)
    except Exception as e:
        print(f"TTS Error: {e}")
        return analysis_result, None  # If TTS fails, return only text

    return analysis_result, tts_path

# Creating the Gradio interface
iface = gr.Interface(
    fn=analyze_news,
    inputs=gr.Textbox(label="Enter Company Name"),
    outputs=[gr.Textbox(label="Analysis Result"), gr.Audio(label="Hindi Audio")],
    title="Company News Analyzer",
    description="Extracts key details, performs sentiment & comparative analysis, and generates Hindi TTS."
)

# Launching the app
if __name__ == "__main__":
    iface.launch(share=True)  # Enables public link
