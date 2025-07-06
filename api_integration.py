import os
import google.generativeai as genai

# Use your environment variable or replace with your actual API key (not recommended for production)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_insights(data_df):
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Extract a sample (top 10 rows) for analysis
    data = data_df.head(10).to_dict(orient='records')

    # Prompt for Gemini
    prompt = f"""
You are an expert travel analyst.

Below is historical flight route data showing passenger volume and ticket prices per route for different years:

{data}

1. What are the most popular routes overall?
2. What trend do you observe in passenger volume over time?
3. Provide 3 key market insights.

📌 Format your response using valid HTML tags like <strong>, <ul>, <li>, <br>, etc., for display in a webpage. Do not use Markdown syntax.
"""

    # Generate response
    response = model.generate_content(prompt)
    return response.text
