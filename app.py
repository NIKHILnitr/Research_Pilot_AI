import streamlit as st
from utils.pdf_loader import extract_text_from_pdf
from utils.summarizer import (
    summarize_paper,
    explain_simple,
    key_takeaways,
    answer_question
)
from utils.vector_store import create_vector_store, retrieve_chunks

st.set_page_config(
    page_title="ResearchPilot",
    page_icon="📚",
    layout="wide"
)

# ==========================
# Sidebar
# ==========================

with st.sidebar:

    st.title("📚 ResearchPilot")

    st.markdown("### AI Research Copilot")

    st.markdown("---")

    st.markdown("### 🚀 Features")

    st.markdown("""
- 📄 Research Summary
- 🧠 Explain Like I'm 15
- ⭐ Key Takeaways
- ❓ AI Question Answering
- ⚡ Semantic Search
""")

    st.markdown("---")

    st.info(
        "Powered by Google Gemini + FAISS + Sentence Transformers"
    )

# ==========================
# Main Title
# ==========================

st.title("📚 ResearchPilot")

st.markdown(
"""
### AI-Powered Research Copilot

Upload any research paper and instantly:

- 📄 Generate structured summaries
- 🧠 Explain difficult concepts simply
- ⭐ Extract key insights
- ❓ Ask questions using AI
"""
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)

# ==========================
# PDF Uploaded
# ==========================

if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    with st.spinner("📖 Reading PDF..."):

        text = extract_text_from_pdf(uploaded_file)

    if len(text.strip()) == 0:

        st.error("No readable text found.")

        st.stop()

    # ======================
    # Statistics
    # ======================

    word_count = len(text.split())

    chunk_count = max(1, len(text) // 800)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📄 Characters",
        f"{len(text):,}"
    )

    col2.metric(
        "📝 Words",
        f"{word_count:,}"
    )

    col3.metric(
        "🧩 Chunks",
        chunk_count
    )

    st.divider()

    # ======================
    # Preview
    # ======================

    with st.expander("📄 Preview Extracted Text"):

        st.text_area(
            "",
            text[:3000],
            height=300
        )

    # ======================
    # Vector DB
    # ======================

    with st.spinner("🧠 Building Knowledge Base..."):

        index, chunks = create_vector_store(text)

    # ======================
    # Tabs
    # ======================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📄 Summary",
            "🧠 Explain Simply",
            "⭐ Key Takeaways",
            "❓ Ask Questions"
        ]
    )

    # ======================
    # SUMMARY
    # ======================

    with tab1:

        with st.spinner("🤖 AI is summarizing the paper..."):

            summary = summarize_paper(text)

        st.markdown(summary)

        st.download_button(
            "📥 Download Summary",
            summary,
            file_name="research_summary.md",
            mime="text/markdown"
        )

    # ======================
    # Explain
    # ======================

    with tab2:

        with st.spinner("🧠 Simplifying research..."):

            explanation = explain_simple(text)

        st.markdown(explanation)

    # ======================
    # Takeaways
    # ======================

    with tab3:

        with st.spinner("⭐ Extracting important insights..."):

            takeaways = key_takeaways(text)

        st.markdown(takeaways)

    # ======================
    # QA
    # ======================

    with tab4:

        st.markdown("### 💡 Suggested Questions")

        suggested = [
            "What is the main contribution?",
            "What methodology is used?",
            "What dataset is used?",
            "What are the limitations?",
            "What future work is suggested?"
        ]

        cols = st.columns(2)

        for i, q in enumerate(suggested):

            if cols[i % 2].button(q):

                context = retrieve_chunks(
                    index,
                    chunks,
                    q
                )

                answer = answer_question(
                    context,
                    q
                )

                st.success(answer)

        st.divider()

        question = st.text_input(
            "Ask your own question"
        )

        if question:

            with st.spinner("🔍 Searching paper..."):

                context = retrieve_chunks(
                    index,
                    chunks,
                    question
                )

                answer = answer_question(
                    context,
                    question
                )

            st.markdown("### 🤖 Answer")

            st.success(answer)

st.divider()

st.caption(
    "Built with ❤️ using Streamlit, Google Gemini, FAISS and Sentence Transformers."
)