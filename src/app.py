import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from src.gemini_llm import GeminiLLM
from src.news_fetcher import get_all_news
from src.config import NEWS_CONFIG
from dotenv import load_dotenv
import google.generativeai as genai
import os


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

llm = GeminiLLM()
news_template = """
Summarize the following list of news articles in a short paragraph (2-3 sentences) without mentioning sources, keeping it simple and engaging.

News Articles:
{text}
Summary:
"""
news_prompt = PromptTemplate(input_variables=["text"], template=news_template)
news_chain = LLMChain(prompt=news_prompt, llm=llm)

TECH_SUBCATEGORIES = ["ai", "hardware", "software", "cybersecurity", "space"]

def main():
    """Streamlit app for News Summarizer & Chat."""
    st.title("News Summarizer & Chat")
    st.write("Select a news category to get a summary, then chat about it below!")

    if "news_text" not in st.session_state:
        st.session_state.news_text = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "sub_category" not in st.session_state:
        st.session_state.sub_category = "None"
    if "detailed_summary" not in st.session_state:
        st.session_state.detailed_summary = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    categories = ["All"] + list(NEWS_CONFIG["sources"].keys())
    category = st.selectbox("Choose a news category:", categories)

    if st.button("Get News"):
        with st.spinner(f"Fetching and summarizing {'the latest ' + category.lower() + ' ' if category != 'All' else 'all '}news..."):
            st.session_state.news_text = get_all_news(category.lower() if category != "All" else None)
            if len(st.session_state.news_text.strip()) < 50:
                st.error("No substantial news fetched. Check the RSS feeds or try again.")
                st.session_state.summary = ""
            else:
                st.session_state.summary = news_chain.invoke({"text": st.session_state.news_text})["text"]
                st.session_state.sub_category = "None"
                st.session_state.detailed_summary = ""

    if st.session_state.summary:
        st.subheader("Summary")
        st.write(st.session_state.summary)

        if category.lower() == "technology":
            sub_category = st.selectbox(
                "Interested in a specific area of technology?",
                ["None"] + TECH_SUBCATEGORIES,
                index=(TECH_SUBCATEGORIES.index(st.session_state.sub_category) + 1 if st.session_state.sub_category in TECH_SUBCATEGORIES else 0)
            )
            if sub_category != st.session_state.sub_category:
                st.session_state.sub_category = sub_category
                if sub_category != "None":
                    with st.spinner(f"Generating detailed {sub_category} summary..."):
                        sub_prompt = f"From this technology news:\n{st.session_state.news_text}\nFocus on {sub_category} aspects and provide a detailed summary."
                        st.session_state.detailed_summary = llm._call(sub_prompt)

            if st.session_state.detailed_summary:
                st.subheader(f"Detailed {st.session_state.sub_category.capitalize()} Summary")
                st.write(st.session_state.detailed_summary)

    if st.session_state.news_text and st.checkbox("Show raw news text"):
        st.text_area("Raw News", st.session_state.news_text, height=200)

    st.subheader("Chat About the News")
    user_input = st.text_input("Your message:", key="chat_input")
    if st.button("Send"):
        if user_input:
            if st.session_state.news_text:
                chat_prompt = f"Here's the recent news I summarized:\n{st.session_state.news_text}\n\nUser: {user_input}\nResponse:"
                response = llm._call(chat_prompt)
            else:
                chat_prompt = f"User: {user_input}\nResponse:"
                response = llm._call(chat_prompt)
            st.session_state.chat_history.append({"user": user_input, "ai": response})
    
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**AI:** {chat['ai']}")

if __name__ == "__main__":
    main()