# CIRNO Math and Science Agent

A specialized AI agent for STEM (Science, Technology, Engineering, and Mathematics) topics within the CIRNO multi-agent system. This agent provides expert knowledge in science, mathematics, engineering, economics, history, and geology through integration with Wolfram Alpha and academic research databases.

## ✨ Features

- **🔍 Scientific Information Retrieval**: Search for real-time scientific data, mathematical calculations, engineering concepts, historical facts, and geological information using Wolfram Alpha
- **📚 Academic Research Access**: Discover and summarize research papers from the OpenAlex database
- **⚡ Streaming Responses**: Real-time streaming of agent responses for better user experience
- **🤖 Multi-tool Agent Architecture**: Built on LangChain with intelligent tool selection and execution
- **🌐 A2A Framework Integration**: Compatible with the CIRNO multi-agent ecosystem via the a2a framework

## 🚀 Quick Start

### Prerequisites
- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/StudentAssistantTeam/CIRNO_MathAndScienceAgent.git
   cd CIRNO_MathAndScienceAgent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment variables**
   Create a `cirno_math_and_science_agent.env` file in the project root with the following variables:
   ```env
   # LLM Configuration
   LLM_MODEL_NAME="gpt-4o"
   LLM_BASE_URL="https://api.openai.com/v1"
   LLM_API_KEY="your-openai-api-key"
   LLM_PROVIDER="openai"

   # Wolfram Alpha API
   WOLFRAM_APP_ID="your-wolfram-alpha-app-id"

   # OpenAlex API
   OPENALEX_API="your-openalex-api-key"

   # Server Configuration
   A2A_HOST="0.0.0.0"
   A2A_PORT=4000
   ```

### Running the Agent

**Using the installed script**
```bash
uv run science_and_math_agent_app
```

The agent will start a server on `http://localhost:4000` (or the configured host/port).

## 📋 Usage

### As a Standalone Agent

The agent provides two main skills:

1. **STEM Info Searching Tool**: For general science, math, engineering, history, and geology queries
   - Examples: "Give me some information about Jupiter", "Find me some information about France", "Solve 2^x=114514"

2. **Research Paper Searching Tool**: For academic research and theoretical information
   - Examples: "Show me the researches about machine learning for drug discovery", "Show me about the definition of Quantum Physics"

### Integration with CIRNO System

The agent is designed to work within the CIRNO multi-agent framework. It exposes an A2A-compatible API endpoint that can be discovered and utilized by other agents in the system.

## 🛠️ Technical Architecture

### Core Components

- **`agent.py`**: Main agent class with LangChain integration and streaming capabilities
- **`tool.py`**: Tool implementations for Wolfram Alpha and OpenAlex integration
- **`request_wolfram.py`**: Wolfram Alpha API client
- **`essay_manager.py`**: OpenAlex integration and PDF processing
- **`agent_executor.py`**: A2A request handler adapter
- **`config.py`**: Configuration management using Pydantic Settings

### Agent Flow

```
User Query → Agent → Tool Selection → External APIs → Response Generation → Stream to User
```

### Available Tools

1. **`search_math_and_science_info`**: Queries Wolfram Alpha for scientific and mathematical information
   - Supports complex calculations
   - Provides real-time data
   - Handles multiple queries simultaneously

2. **`academics_searcher`**: Searches OpenAlex for academic papers
   - Retrieves paper metadata
   - Downloads and summarizes PDFs
   - Extracts key information with AI summarization

3. **`final_answer`**: Signal to end tool-calling and generate final response

## ⚙️ Configuration

### Configuration

- **Database Storage**: Enable database persistence for tasks and notifications by setting `USE_DB_TASK_STORE=true`, `USE_DB_PUSH_NOTIFICATION=true` and providing `DB_URL`
- **Custom LLM Providers**: Support for any OpenAI-compatible API via `LLM_PROVIDER` and `LLM_BASE_URL`

## 🔧 Development

### Project Structure
```
cirno_math_and_science_agent/
├── __init__.py
├── __main__.py          # Entry point and server setup
├── agent.py             # Main agent implementation
├── agent_executor.py    # A2A request handler
├── config.py            # Configuration management
├── data_models.py       # Pydantic models
├── essay_manager.py     # OpenAlex integration
├── logger_config.py     # Logging setup
├── prompts.py           # System prompts and tool descriptions
├── request_wolfram.py   # Wolfram Alpha client
└── tool.py              # LangChain tool implementations
```

## 📊 Example Queries

### Science and Math Queries
- "What is the melting point of gold?"
- "Calculate the derivative of x^2 + 3x - 5"
- "What's the population of Japan in 2024?"
- "Explain the theory of relativity"

### Research Paper Queries
- "Find recent papers on quantum computing"
- "Show me research about climate change mitigation"
- "What are the latest developments in CRISPR technology?"

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.