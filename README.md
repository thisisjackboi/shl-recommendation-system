
# SHL Assessment Recommendation System

## 📖 Overview
This project implements a recommendation system specifically designed for suggesting SHL assessments based on user-provided job descriptions or query terms. The core functionality involves embedding-based semantic similarity computations and evaluation using precision and recall metrics.

## 🚀 Features
- **Semantic Recommendation**: Provides relevant SHL assessments based on user input.
- **Embedding Support**: Uses modern NLP embedding techniques.
- **API Integration**: Offers recommendations through a REST API.
- **Evaluation Metrics**: Calculates Mean Average Precision (MAP) and Recall for accuracy measurement.
- **Interactive Frontend**: Modern and intuitive web interface with dynamic search capabilities and theme toggles using streamlit.

## 📁 Project Structure

```
shl_assesment_recommender/
├── api.py                         # REST API endpoints
├── streeamlit_app.py              #for hosting
├── evaluation.py                  # Recommendation evaluation script
├── new_scrapper2.py               # Web scraping utility
├── recommender.py                 # Recommendation engine
├── shl_assessments.csv            # Dataset in CSV format
├── shl_assessments.json           # Dataset in JSON format
├── test.ipynb                     # Jupyter notebook for exploratory analysis
├── static/                        # Frontend static files
│   ├── script.js
│   └── style.css
└── templates/                     # HTML Templates
    └── index.html
```

## 🛠 Installation & Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/shl-recommendation-system.git
cd shl-recommendation-system
```

### Step 2: Setup Python Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

### Start the API server
```bash
python api.py
```

### Accessing the Frontend
Open `templates/index.html` directly in your browser, or serve using a local server:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/templates/index.html` in a browser.

## 🌐 API Documentation

**Endpoint:**
```
POST /recommend
```

**Request Example:**
```json
{
  "query": "software engineer",
  "num_results": 5
}
```

**Response Example:**
```json
{
  "recommendations": [
    {
      "Assessment Name": "Agile Software Development",
      "URL": "https://www.shl.com/products/product-catalog/view/agile-software-development/",
      "Test Type": "Knowledge & Skills",
      "Score": 0.78
    }
  ]
}
```

## 📊 Dataset Description

| Column Name     | Description                             |
|-----------------|-----------------------------------------|
| Assessment Name | Name of the SHL assessment              |
| URL             | Direct URL to the assessment page       |
| Test Type       | Assessment category (knowledge, skills) |
| Duration        | Duration check                          |
| test type       | Brief description of assessment type    |


## 💻 Frontend Functionality

- **index.html** – Frontend UI
- **script.js** – Handles theme toggle, API requests, and rendering
- **style.css** – Custom glassmorphic and responsive design

## 🧪 Evaluation

Run evaluation metrics:
```bash
python evaluation.py
```

Outputs metrics like MAP@3 and Recall@3.



## 📜 License
MIT License

## 📧 Contact
For queries, contact: [your.email@asrafulhhaque@gmail.com]
