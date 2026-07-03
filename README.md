# 🚀 LinkedIn Post Generator (Gen AI & LLM Architecture)

An end-to-end Generative AI application designed to dynamically generate LinkedIn posts that mimic the unique writing style, formatting, and tone of specific industry influencers. 

Instead of relying on generic LLM prompts that produce robotic content, this project utilizes a custom data extraction pipeline, metadata enrichment, and **Few-Shot Prompting** via LangChain and Llama 3.2 to generate highly personalized, human-sounding content.

---

## 🌟 Key Features

*   **Custom Web Scraper:** Built with Selenium and BeautifulSoup to bypass dynamic DOM loading. It safely authenticates via session cookies and manually replaces HTML tags with `\n` to perfectly preserve paragraph structure and line breaks.
*   **Automated Data Enrichment:** Raw posts are passed through an LLM to extract key metadata (Topic Tags, Post Length, and Language), structured into a Pandas DataFrame.
*   **Dynamic Few-Shot Learning:** When a user inputs their desired parameters, the system queries the Pandas dataset to retrieve the most relevant historical posts to use as context examples.
*   **Lightning-Fast Inference:** Powered by Meta's Llama 3.2 running on Groq Cloud for near-instant generation.
*   **Interactive UI:** A clean frontend (built with Streamlit) allowing users to select topics, post length, and language to generate content in seconds.

---

## 🏗️ System Architecture

1.  **Data Extraction Layer (`fetching_post.py`):** Connects to LinkedIn, injects the `li_at` cookie to bypass login walls, scrolls dynamically, parses the HTML, cleans the text, and exports raw data to JSON.
2.  **Pre-processing Layer:** Takes the raw JSON, unifies topic tags, categorizes line counts into lengths (Short, Medium, Long), and prepares a structured data dictionary.
3.  **Retrieval Engine (`few_shot.py`):** Loads the processed JSON into a Pandas DataFrame. Filters and retrieves historical posts matching the user's exact criteria to serve as few-shot examples.
4.  **Generative AI Engine:** LangChain constructs a dynamic prompt containing the system instructions, user parameters, and the few-shot examples, feeding it to the Groq API.
5.  **User Interface:** The frontend application where users interact with the backend infrastructure.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.10+
*   **Web Scraping:** Selenium, BeautifulSoup4, RegEx
*   **Data Processing:** Pandas, JSON
*   **Generative AI Orchestration:** LangChain
*   **LLM Provider:** Groq Cloud (Llama 3.2 90B)
*   **Frontend:** Streamlit

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/LinkedIn-Post-Generator.git](https://github.com/YourUsername/LinkedIn-Post-Generator.git)
cd LinkedIn-Post-Generator
