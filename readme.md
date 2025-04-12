# 🗞️ News Summarizer & Chat

A Streamlit app that fetches real-time news from various sources, summarizes them using **Google Gemini AI**, and lets you chat about the news. Ideal for users who want quick, smart insights without reading dozens of articles.

![Demo](screenshorts/demo.mp4)

## ✨ Features

- ✅ Fetches news from multiple categories using RSS
- 🧠 Summarizes articles using LangChain + Gemini Pro
- 📚 Explore tech subtopics like AI, hardware, and space
- 💬 Built-in chat to discuss summaries or dive deeper
- 🔎 Option to view full raw news content

## 🧭 User Flow

See the Figma flowchart for an overview of how the app works:

📌 [Figma Flowchart](https://www.figma.com/board/bRqdVxbwbW3wXfIl0tDbP5/News-Summarizer-%26-Chat?node-id=0-1&t=T6l3JVIva6vOWfzU-1)

## 📁 Project Structure

```
.
├── run.py                 # start
├── .env                   # Environment variables
├── screenshort/
│   └── demo.mp4           # App demo video
├── src/
│   ├── gemini_llm.py      # LLM wrapper for Gemini
    ├── app.py                  # Streamlit entry point
│   ├── news_fetcher.py    # News pulling logic
│   └── config.py          # RSS config (sources & categories)
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/news-summarizer-chat.git
cd news-summarizer-chat
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file and paste your Google Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

### 4. Run the App

```bash
streamlit run app.py
```

## 🧠 Built With

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Google Gemini Pro](https://ai.google.dev/)
- RSS feeds (via `feedparser` or similar libraries)

## 🎥 Demo

Watch the [demo video](screenshort/demo.mp4) for a full walkthrough.

## 🤝 Contributing

Feel free to fork the project and submit pull requests. For major features or bugs, open an issue to start a discussion first.

---

📰 Stay informed. Stay smart.
