# 📄 GLR Pipeline - Insurance Template Filler

> **Automate insurance template filling using photo reports and AI-powered data extraction**

A Streamlit-based application that leverages Large Language Models (LLMs) to intelligently extract data from insurance photo reports (PDFs) and automatically populate insurance templates (.docx).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🎯 Overview

The **GLR Pipeline** (General Ledger Report Pipeline) is designed to streamline the insurance claims processing workflow by:

1. **Extracting text** from photo reports in PDF format
2. **Analyzing templates** to identify fields that need to be filled
3. **Using AI** (LLMs via Groq API) to intelligently match and extract data
4. **Populating templates** with extracted information
5. **Generating** a ready-to-use filled document

### Key Features

- 🤖 **AI-Powered Extraction**: Uses Llama 3.3 70B, Mixtral, and other powerful models
- 📄 **Multi-Document Support**: Process multiple PDF reports simultaneously
- 📝 **Template Preservation**: Maintains original document formatting
- 🎨 **Modern UI**: Clean, intuitive Streamlit interface
- 📥 **Instant Download**: One-click download of filled documents
- 🆓 **Free LLM Access**: Uses Groq's generous free tier (14,400 requests/day)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit Frontend                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────────┐   │
│  │ Template      │  │ PDF Reports   │  │ API Key Config    │   │
│  │ Upload (.docx)│  │ Upload (PDFs) │  │ (Groq)            │   │
│  └───────┬───────┘  └───────┬───────┘  └─────────┬─────────┘   │
└──────────┼──────────────────┼────────────────────┼──────────────┘
           │                  │                    │
           ▼                  ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                     Backend Processing                            │
│                                                                   │
│  ┌─────────────────┐         ┌──────────────────────────────┐   │
│  │ PDF Extractor   │         │ DOCX Parser                  │   │
│  │ (PyMuPDF)       │         │ (python-docx)                │   │
│  └────────┬────────┘         └──────────────┬───────────────┘   │
│           │                                  │                   │
│           ▼                                  ▼                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    LLM Processor                            │ │
│  │  • Sends extracted text + template to Groq API              │ │
│  │  • Uses Llama 3.3 70B for intelligent extraction            │ │
│  │  • Returns structured JSON with field-value mappings        │ │
│  └────────────────────────────┬───────────────────────────────┘ │
│                               │                                  │
│                               ▼                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Template Filler                           │ │
│  │  • Maps extracted values to template fields                 │ │
│  │  • Handles tables, paragraphs, headers                      │ │
│  │  • Preserves document formatting                            │ │
│  └────────────────────────────┬───────────────────────────────┘ │
└───────────────────────────────┼─────────────────────────────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │  Filled .docx Output  │
                     │  (Download Ready)     │
                     └──────────────────────┘
```

---

## 📁 Project Structure

```
Task 3/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
├── .gitignore                  # Git ignore file
├── .env                        # API key configuration (create this)
├── modules/
│   ├── __init__.py            # Module exports
│   ├── pdf_extractor.py       # PDF text extraction (PyMuPDF)
│   ├── docx_parser.py         # DOCX template parsing
│   ├── llm_processor.py       # Groq LLM API integration
│   └── template_filler.py     # Template population logic
│
└── Task 3 - GLR Pipeline/      # Example data
    ├── Example 1 - USAA/
    ├── Example 2 - Wayne-Elevate/
    └── Example 3 - Guide One - Eberl/
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/glr-pipeline.git
   cd glr-pipeline
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a FREE Groq API Key:**
   - Visit [https://console.groq.com/keys](https://console.groq.com/keys)
   - Sign up with Google or email (no credit card required)
   - Create a new API key
   - Copy the key

4. **Create `.env` file (optional):**
   ```bash
   echo "GROQ_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser:**
   - The app will automatically open at `http://localhost:8501`

---

## 📖 How to Use

### Step 1: Configure API Key
Enter your Groq API key in the sidebar (or set it in `.env` file).

### Step 2: Upload Template
Upload your insurance template in `.docx` format.

### Step 3: Upload Photo Reports
Upload one or more PDF photo reports.

### Step 4: Process
Click "Process Documents & Fill Template" to start the AI-powered extraction.

### Step 5: Download
Review the extracted data and download your filled document.

---

## 🤖 Supported LLM Models

The application uses Groq's free tier models:

| Model | Description | Best For |
|-------|-------------|----------|
| `llama-3.3-70b-versatile` | Most capable | Complex documents |
| `llama-3.1-8b-instant` | Fastest | Quick processing |
| `mixtral-8x7b-32768` | Balanced | General use |
| `gemma2-9b-it` | Efficient | Moderate complexity |

---

## 🧪 Testing with Examples

The project includes 3 example datasets:

1. **Example 1 - USAA**: USAA 800 Claims template
2. **Example 2 - Wayne-Elevate**: Elevate Wayne template
3. **Example 3 - Guide One - Eberl**: GuideOne Eberl template

Each example contains:
- `Input/`: Template (.docx) and photo report (.pdf)
- `Output/`: Expected completed document for comparison

---

## ⚠️ Troubleshooting

### "API request failed"
- Verify your Groq API key is correct
- Check internet connectivity
- Try a different model

### "Could not extract text from PDF"
- Ensure PDF contains extractable text (not just images)
- For scanned documents, OCR preprocessing may be needed

### "Failed to parse LLM response"
- Try processing again
- Switch to a different model

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Web framework
- [Groq](https://groq.com/) - Fast LLM inference
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing
- [python-docx](https://python-docx.readthedocs.io/) - DOCX manipulation

---

*Built for ProductizeTech Task 3 - GLR Pipeline with Streamlit*
