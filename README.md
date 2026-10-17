# 💄 Beauty Creator Suite — AI Content & Brand PR Engine

An all-in-one AI platform built for beauty creators, influencers, and digital marketing agencies. Powered by **Streamlit** and **Groq LLM** for ultra-fast generation of viral Instagram Reel scripts, FTC/ASCI-compliant captions, targeted hashtags, and high-converting brand PR pitches.

---

## ✨ Features

- 🎬 **Viral Hook Generator:** Generates 3 scroll-stopping hook options (0–3 seconds) for beauty Reels.
- 📜 **30-Second Reel Script:** Line-by-line visual action cues paired with voiceover timing.
- 📝 **High-Converting Captions:** Structured Instagram captions with step-by-step product application guides.
- 🏷️ **Strategic Hashtags:** 30 categorized hashtags grouped by niche, product type, skin concerns, and regional trends.
- ⚖️ **Compliance Ready:** Includes ready-to-copy ASCI / FTC disclosure statements for sponsored content.
- 📩 **Brand PR Pitch Generator:** Drafts targeted outreach letters for PR Gifting Packages, Paid Partnerships, and Long-term Brand Ambassador roles.

---

## 🛠️ Tech Stack

- **Frontend / Framework:** [Streamlit](https://streamlit.io/)
- **LLM Engine:** [Groq API](https://groq.com/)
- **Language:** Python 3.9+

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.9 or higher installed on your machine.

### 2. Clone the Repository
```bash
git clone https://github.com/Mou-arc/BeautySuite
cd BeautySuite
```

### 3. Create a Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up API Key
Navigate to the `.streamlit` directory.

Duplicate or rename `secrets.toml.example` to `secrets.toml`.

Open `.streamlit/secrets.toml` and add your Groq API key:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

### 6. Run the Application
```bash
streamlit run app.py
```

## 📁 Project Structure
```
├── .streamlit/
│   ├── secrets.toml         # Local secrets (Ignored by Git)
│   └── secrets.toml.example # Public API key template
├── .gitignore               # Ignored local & system files
├── app.py                   # Main Streamlit application
├── requirements.txt         # Project Python dependencies
└── README.md                # Project documentation
```

## 📄 License
This project is delivered as a turnkey codebase. Free to rebrand, customize, and deploy for personal or client use.