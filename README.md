# 🚀 LinkedIn Post Generator using LLMs

This project uses LLMs to analyze, enrich and generate professional-grade LinkedIn posts. It transforms raw post data into semantically rich content through intelligent tagging, emoji enhancement, and hashtag extraction. Users can easily generate new posts through an intuitive Streamlit interface.

---

## 🧠 Features

- 📌 Preprocess and enrich real LinkedIn posts with semantic metadata
- 🏷️ Automatically detect and unify topic tags
- ✍️ Generate new LinkedIn-style posts using few-shot learning and LLMs
- 💬 Add relevant emojis and extract hashtags using NLP
- ⚡ Uses **Groq's `llama-3.2-90b-vision-preview`** model for ultra-fast, high-quality generation
- 🖼️ Streamlit-based UI for easy interaction and post generation

---

## 📁 Data Flow Overview

```text
raw_posts.json ──▶ preprocess.py ──▶ processed_posts.json
                                ▲              │
                         few_shot.py ◀─────────┘
                                │
            post_generator.py ◀─┘ (uses LLM + examples + emojis + hashtags)
                                │
                       main.py (Streamlit UI)
```

## 🔄 Detailed Component Flow

### 📄 `raw_posts.json`
- Contains original, unprocessed LinkedIn post data.
- Structure:
```json
{
  "text": "Example LinkedIn post content...",
  "engagement": 345
}
```

---

### 🛠️ `preprocess.py`
- Adds the following metadata to each post:
  - `line_count`
  - `language` (English / Hinglish)
  - Up to 2 `tags`
- Unifies similar tags across all posts.
- Saves the output to `processed_posts.json`.

---

### 📌 `processed_posts.json`
- Output file after preprocessing.
- Contains structured metadata for post generation:
```json
{
  "text": "...",
  "engagement": 345,
  "line_count": 3,
  "language": "English",
  "tags": ["Motivation", "Career Advice"]
}
```

---

### 🔍 `few_shot.py`
- Loads `processed_posts.json`
- Filters and returns few-shot examples based on:
  - Language
  - Length (short/medium/long)
  - Tags
- These examples are used to guide the LLM when generating new posts.

---

### 🤖 `post_generator.py`
- Generates new posts based on user selections.
- Uses:
  - Few-shot examples
  - Prompt + LLM (via Groq)
- LLM model used: **`llama-3.2-90b-vision-preview`**
- Enhances output with:
  - Relevant emojis (based on post theme)
  - Hashtags extracted from text using spaCy

---

### 🎛️ `main.py`
- Streamlit UI for user interaction.
- Users can:
  - Select post language
  - Choose topic/tag
  - Set post length
  - Click to generate a fresh post

---

## 🖼️ Streamlit UI Screenshots

![Streamlit UI](https://github.com/user-attachments/assets/74accd8d-6b98-4811-887f-80133fb8a92a)

![Streamlit UI](https://github.com/user-attachments/assets/54e15a18-1203-445b-bde3-a53c5fb22266)

![Streamlit UI](https://github.com/user-attachments/assets/ab435c98-b347-4ddb-b7fb-12c5aa877176)

---

## 🧪 Getting Started

### ✅ Prerequisites

- Python 3.10+
- Groq API Key (from https://console.groq.com)
- Access to **`llama-3.2-90b-vision-preview`** model

---

### 📦 Installation

```bash
git clone https://github.com/your-username/linkedin-post-generator.git
cd linkedin-post-generator

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

### 🔐 Environment Setup

Create a `.env` file in the root with your Groq API Key:

```env
GROQ_API_KEY=your_key_here
```

---

### 🧹 Preprocess Data

```bash
python preprocess.py
```

---

### 🚀 Launch the App

```bash
streamlit run main.py
```
