"""
GLR Pipeline - Streamlit Application
Automates insurance template filling using photo reports and LLMs.
"""

import streamlit as st
from io import BytesIO
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.pdf_extractor import extract_text_from_pdf, extract_text_from_multiple_pdfs
from modules.docx_parser import parse_template, get_template_text, get_document_structure
from modules.llm_processor import extract_field_values, get_available_models, LLMProcessor
from modules.template_filler import fill_template, save_filled_template


# Page Configuration
st.set_page_config(
    page_title="GLR Pipeline - Insurance Template Filler",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .step-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
    }
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #3b82f6;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application entry point."""
    
    # Header
    st.markdown('<h1 class="main-header">📄 GLR Pipeline</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Automate insurance template filling using photo reports and AI</p>', unsafe_allow_html=True)
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Get API key from environment variable
        default_api_key = os.getenv("GROQ_API_KEY", "")
        
        # API Key Input
        api_key = st.text_input(
            "Groq API Key",
            value=default_api_key,
            type="password",
            help="Get your FREE API key from https://console.groq.com/keys"
        )
        
        # Model Selection
        available_models = get_available_models()
        model_names = {
            "llama-3.3-70b-versatile": "Llama 3.3 70B (Most Capable)",
            "llama-3.1-8b-instant": "Llama 3.1 8B (Fastest)",
            "mixtral-8x7b-32768": "Mixtral 8x7B",
            "gemma2-9b-it": "Gemma 2 9B",
        }
        
        selected_model = st.selectbox(
            "Select LLM Model",
            options=available_models,
            format_func=lambda x: model_names.get(x, x),
            help="Choose the AI model for text extraction"
        )
        
        st.divider()
        
        # Instructions
        st.header("📖 How to Use")
        st.markdown("""
        1. **Get API Key** - [Groq Console](https://console.groq.com/keys) (FREE!)
        2. **Upload Template** - Your insurance template (.docx)
        3. **Upload Reports** - Photo reports in PDF format
        4. **Process** - Click to extract and fill
        5. **Download** - Get your filled document
        """)
        
        st.divider()
        st.caption("Built with ❤️ using Streamlit & Groq")
    
    # Main Content Area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.markdown('<p class="step-title">📋 Step 1: Upload Insurance Template</p>', unsafe_allow_html=True)
        
        template_file = st.file_uploader(
            "Upload your insurance template",
            type=["docx"],
            help="Upload the .docx template file that needs to be filled",
            key="template_uploader"
        )
        
        if template_file:
            st.success(f"✅ Template uploaded: {template_file.name}")
            
            # Show template preview
            with st.expander("🔍 Preview Template Structure"):
                try:
                    template_bytes = template_file.read()
                    template_file.seek(0)
                    doc = parse_template(BytesIO(template_bytes))
                    structure = get_document_structure(doc)
                    
                    st.write(f"**Paragraphs:** {structure['paragraphs']}")
                    st.write(f"**Tables:** {structure['tables']}")
                    if structure['table_info']:
                        for table in structure['table_info']:
                            st.write(f"  - Table {table['index'] + 1}: {table['rows']} rows × {table['cols']} cols")
                except Exception as e:
                    st.error(f"Could not parse template: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.markdown('<p class="step-title">📸 Step 2: Upload Photo Reports</p>', unsafe_allow_html=True)
        
        pdf_files = st.file_uploader(
            "Upload photo report PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload one or more PDF photo reports",
            key="pdf_uploader"
        )
        
        if pdf_files:
            st.success(f"✅ {len(pdf_files)} PDF(s) uploaded")
            for pdf in pdf_files:
                st.write(f"  • {pdf.name}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Process Button
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Validation
    ready_to_process = api_key and template_file and pdf_files
    
    if not ready_to_process:
        missing = []
        if not api_key:
            missing.append("API Key")
        if not template_file:
            missing.append("Template (.docx)")
        if not pdf_files:
            missing.append("Photo Reports (PDF)")
        
        st.warning(f"⚠️ Please provide: {', '.join(missing)}")
    
    process_button = st.button(
        "🚀 Process Documents & Fill Template",
        disabled=not ready_to_process,
        use_container_width=True
    )
    
    # Processing Logic
    if process_button and ready_to_process:
        try:
            # Progress container
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Extract text from PDFs
                status_text.text("📖 Extracting text from photo reports...")
                progress_bar.progress(10)
                
                pdf_contents = []
                for pdf in pdf_files:
                    pdf_bytes = pdf.read()
                    pdf.seek(0)
                    pdf_contents.append((pdf.name, pdf_bytes))
                
                combined_report_text = extract_text_from_multiple_pdfs(pdf_contents)
                progress_bar.progress(30)
                
                # Step 2: Parse template
                status_text.text("📋 Analyzing template structure...")
                template_bytes = template_file.read()
                template_file.seek(0)
                template_doc = parse_template(BytesIO(template_bytes))
                template_text = get_template_text(template_doc)
                progress_bar.progress(45)
                
                # Step 3: Extract field values using LLM
                status_text.text("🤖 AI is extracting information from reports...")
                progress_bar.progress(50)
                
                field_values = extract_field_values(
                    template_text=template_text,
                    report_text=combined_report_text,
                    api_key=api_key,
                    model=selected_model
                )
                progress_bar.progress(75)
                
                # Step 4: Fill template
                status_text.text("✍️ Filling template with extracted data...")
                
                # Re-parse template for filling (we need a fresh copy)
                template_doc_fill = parse_template(BytesIO(template_bytes))
                filled_doc = fill_template(template_doc_fill, field_values)
                progress_bar.progress(90)
                
                # Step 5: Generate output
                status_text.text("📄 Generating output document...")
                output_buffer = save_filled_template(filled_doc)
                progress_bar.progress(100)
                
                status_text.text("✅ Processing complete!")
            
            # Success Section
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("### ✅ Document Processing Complete!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Results in columns
            result_col1, result_col2 = st.columns([1, 1])
            
            with result_col1:
                st.subheader("📊 Extracted Data")
                with st.expander("View Extracted Fields", expanded=True):
                    for field, value in field_values.items():
                        st.markdown(f"**{field}:** {value}")
            
            with result_col2:
                st.subheader("📥 Download Result")
                
                # Generate filename
                output_filename = f"Filled_{template_file.name}"
                
                st.download_button(
                    label="⬇️ Download Filled Template",
                    data=output_buffer.getvalue(),
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                
                st.info(f"📄 Output file: **{output_filename}**")
            
            # Show extracted text (collapsible)
            with st.expander("🔍 View Extracted Report Text"):
                st.text_area(
                    "Combined Report Text",
                    combined_report_text,
                    height=300,
                    disabled=True
                )
        
        except Exception as e:
            st.error(f"❌ Error during processing: {str(e)}")
            
            with st.expander("🔧 Debug Information"):
                import traceback
                st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
