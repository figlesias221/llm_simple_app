# LLM Simple App with Streaming

> Simple Flask web application demonstrating real-time streaming of LLM responses from OpenAI ChatGPT

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991)](https://openai.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.0+-orange)](https://python.langchain.com/)

## 🎯 Overview

This is a simple Flask web application that demonstrates how to stream responses from OpenAI's ChatGPT API in real-time using Server-Sent Events (SSE). The app showcases the integration of Flask, LangChain, and OpenAI to create an interactive chat interface with streaming responses.

**Note:** This is a learning/demonstration project. For production use, implement proper security practices including environment variables for API keys, rate limiting, and user authentication.

## ✨ Features

- **Real-time Streaming**: Stream LLM responses token-by-token to the frontend
- **Server-Sent Events**: Uses SSE for efficient real-time communication
- **OpenAI Integration**: Powered by ChatGPT (GPT-3.5-turbo)
- **LangChain Support**: Built with LangChain framework (with examples for vector DB integration)
- **Simple UI**: Clean, minimal interface for testing
- **Flask Backend**: Lightweight Python web server

## 🛠️ Tech Stack

- **Backend**: Flask 2.0+, Flask-RESTful
- **LLM Framework**: LangChain
- **AI Model**: OpenAI GPT-3.5-turbo
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Streaming**: Server-Sent Events (SSE)
- **Optional**: Pinecone (commented out in code for vector database)

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- pip (Python package manager)

## 🚀 Getting Started

### Installation

1. Clone the repository:
```bash
git clone https://github.com/figlesias221/llm_simple_app.git
cd llm_simple_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:

Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Or set it as an environment variable:
```bash
export OPENAI_API_KEY='your_openai_api_key_here'
```

**⚠️ Security Warning**: Never commit API keys to version control. Always use environment variables or a `.env` file (add `.env` to `.gitignore`).

4. Run the application:
```bash
python3 main.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
llm_simple_app/
├── main.py              # Flask server with streaming endpoint
├── templates/
│   └── index.html       # Frontend interface
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md
```

## 🔌 API Endpoints

### `GET /`
Renders the main chat interface.

### `POST /completion`
Streams ChatGPT responses in real-time.

**Request**: Form data (currently uses hardcoded prompt)
**Response**: Server-Sent Events stream
**Content-Type**: `text/event-stream`

## 💡 How It Works

1. **Frontend**: User submits a query through the HTML form
2. **Request**: JavaScript sends POST request to `/completion`
3. **Backend**: Flask receives request and calls OpenAI API with streaming enabled
4. **Streaming**: OpenAI streams response tokens back to Flask
5. **SSE**: Flask yields each token as Server-Sent Events
6. **Display**: JavaScript reads the stream and updates the UI in real-time

## 🔧 Customization

### Change the AI Model

In `main.py`, modify the model parameter:
```python
completion = openai.ChatCompletion.create(
    model="gpt-4",  # Change to gpt-4, gpt-3.5-turbo, etc.
    # ...
)
```

### Modify the System Prompt

Edit the prompt function in `main.py`:
```python
def gen_prompt(query) -> str:
    return f"""Your custom system prompt here.
    Question: {query}
    Context: Your context here
    Answer:
    """
```

### Enable Vector Database (Pinecone)

The code includes commented-out sections for Pinecone integration:
- Uncomment lines 35-88 in `main.py`
- Add your Pinecone API key and configuration
- Install additional dependencies: `pip install pinecone-client`

## 📝 Code Example

**Streaming implementation:**
```python
def stream(input_text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're an assistant."},
            {"role": "user", "content": f"{prompt(input_text)}"},
        ],
        stream=True,
        max_tokens=500,
        temperature=0
    )

    for line in completion:
        if 'content' in line['choices'][0]['delta']:
            yield line['choices'][0]['delta']['content']
```

**Frontend streaming consumption:**
```javascript
const response = await fetch('/completion', {
    method: 'POST',
    body: formData
});
const reader = response.body.getReader();
while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    const text = new TextDecoder().decode(value);
    document.getElementById("result").innerHTML += text;
}
```

## ⚠️ Important Notes

### Security
- **Never commit API keys**: Use environment variables
- **Rate Limiting**: Implement rate limiting for production
- **Input Validation**: Validate and sanitize user inputs
- **Authentication**: Add user authentication for production

### Exposed API Keys in Code
The current `main.py` contains commented-out sections with exposed API keys. These should be:
1. Removed from the code
2. Moved to environment variables
3. Never committed to version control

### Production Readiness
This is a **demonstration project**. For production use, consider:
- Environment variable management (use `python-dotenv`)
- Error handling and logging
- Rate limiting and request throttling
- User authentication and authorization
- HTTPS/SSL
- Database for conversation history
- Proper async handling
- Cost monitoring for API usage

## 🧪 Dependencies

Key dependencies (see `requirements.txt` for full list):
- `flask` - Web framework
- `flask-restful` - REST API extension for Flask
- `openai` - OpenAI API client
- `langchain` - LLM framework
- `python-dotenv` - Environment variable management (recommended)

## 🤝 Contributing

This is a learning project. Feel free to fork and experiment!

## 📄 License

This project is private and not licensed for public use.

## 🔗 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Server-Sent Events Guide](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

---

**Educational Project**: Built to demonstrate LLM streaming with Flask and OpenAI
