# AI GitHub Issue Assistant

An intelligent tool that analyzes and summarizes GitHub issues using AI. This application fetches GitHub issues, processes them with a Large Language Model (LLM), and provides detailed analysis including severity assessment, summaries, and actionable insights.

## 🚀 Features

- **Issue Analysis**: Automatically fetch and analyze any public GitHub issue
- **AI-Powered Insights**: Uses LLM to provide intelligent summaries and recommendations
- **Severity Assessment**: Automatically categorizes issues by severity (Trivial, Low, Medium, High, Critical)
- **History Tracking**: Maintains a database of previously analyzed issues
- **Modern UI**: Clean, intuitive Streamlit-based frontend
- **RESTful API**: FastAPI backend with comprehensive endpoints

## 🏗️ Architecture

The project follows a clean separation of concerns with:

```
ai-github-issue-assistant/
├── backend/           # FastAPI backend service
│   ├── app/
│   │   ├── main.py           # FastAPI application and routes
│   │   ├── github_client.py  # GitHub API integration
│   │   ├── llm_client.py     # LLM integration
│   │   ├── database.py       # Database configuration
│   │   └── models.py         # Data models
│   ├── requirements.txt      # Backend dependencies
│   └── .env                  # Environment variables
├── frontend/          # Streamlit frontend application
│   ├── app.py               # Main Streamlit application
│   ├── assets/              # Static assets
│   ├── requirements.txt     # Frontend dependencies
│   └── .env                 # Frontend environment variables
└── README.md
```

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- An API key for the LLM service (Together AI or similar)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-github-issue-assistant.git
cd ai-github-issue-assistant
```

### 2. Backend Setup

#### Navigate to the backend directory:
```bash
cd backend
```

#### Create a virtual environment:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Configure environment variables:
Create a `.env` file in the `backend` directory with the following variables:

```env
# LLM API Configuration
TOGETHER_API_KEY=your_together_api_key_here

# GitHub API (optional, for higher rate limits)
GITHUB_TOKEN=your_github_token_here

# Database
DATABASE_URL=sqlite:///./db.sqlite3
```

**Note**: 
- Get your Together AI API key from [together.ai](https://together.ai)
- GitHub token is optional but recommended for higher API rate limits

### 3. Frontend Setup

#### Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

#### Create a virtual environment:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

#### Configure environment variables:
Create a `.env` file in the `frontend` directory:

```env
# Backend API URL
BACKEND_URL=http://127.0.0.1:8000
```

## 🚀 Running the Application

### Start the Backend Server

In the `backend` directory with the virtual environment activated:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend API will be available at `http://127.0.0.1:8000`

### Start the Frontend Application

In a new terminal, navigate to the `frontend` directory with the virtual environment activated:

```bash
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`

## 📖 Usage

1. **Access the Application**: Open your browser and go to `http://localhost:8501`

2. **Analyze an Issue**:
   - Enter a GitHub repository URL (e.g., `https://github.com/owner/repo`)
   - Enter the issue number
   - Click "🔍 Analyze Issue"

3. **View Results**:
   - The AI will analyze the issue and provide:
     - Severity assessment (Trivial to Critical)
     - Detailed summary
     - Key insights and recommendations
     - Analysis history

4. **Browse History**: View previously analyzed issues in the history section


## 🧪 Development

### Backend Development

- **FastAPI Documentation**: Visit `http://127.0.0.1:8000/docs` for interactive API documentation
- **Database**: SQLite database with SQLModel ORM


### Frontend Development

- **Streamlit**: Hot reload enabled by default
- **Styling**: Custom CSS can be added to enhance the UI
- **Components**: Modular design for easy feature additions

## 🔍 Troubleshooting

### Common Issues

1. **Backend won't start**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that the `.env` file is properly configured
   - Verify the Together AI API key is valid

2. **Frontend can't connect to backend**:
   - Ensure the backend is running on `http://127.0.0.1:8000`
   - Check the `BACKEND_URL` in the frontend `.env` file


3. **Database issues**:
   - Delete `db.sqlite3` to reset the database
   - Ensure proper write permissions in the backend directory

### Logs and Debugging

- Backend logs are displayed in the terminal running uvicorn
- Frontend logs appear in the Streamlit interface
- Use `--log-level debug` with uvicorn for detailed backend logs


## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the robust backend framework
- [Streamlit](https://streamlit.io/) for the intuitive frontend framework
- [Together AI](https://together.ai/) for LLM services
- [GitHub API](https://docs.github.com/en/rest) for issue data access

**Happy analyzing! 🚀**