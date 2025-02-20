import openai
import os
import requests
from bs4 import BeautifulSoup


client = openai.Client(api_key="Write_Your_key")  # Replace with your actual key

def scrape_website(url):
    """Fetch and extract text content from a website."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join(soup.get_text().split())[:4000]  
            return text if text else "No relevant text found on the page."
        else:
            return f"Failed to retrieve website content. Status Code: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def chat_with_gpt(user_input, website_data):
    """Interacts with OpenAI's GPT-4o API using scraped website content."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Use GPT-4o 
            messages=[
                {"role": "system", "content": "Use the website content to answer user queries."},
                {"role": "user", "content": f"Website Data: {website_data}"},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Chatbot error: {str(e)}"

if __name__ == "__main__":
    url = input("Enter website URL: ")
    website_content = scrape_website(url)
    print("\n Website data retrieved successfully. Start chatting! (Type 'exit' to quit)\n")
    
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chat_with_gpt(user_query, website_content)
        print(f"Bot: {response}\n")