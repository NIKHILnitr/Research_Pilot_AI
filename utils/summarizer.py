from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Change only this if you want another Gemini model
MODEL_NAME = "gemini-flash-latest"


def generate(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Error: {str(e)}"


# =====================================================
# SUMMARY
# =====================================================

def summarize_paper(text):

    prompt = f"""
You are an expert AI Research Assistant.

Analyze the following research paper and generate a professional summary.

Return your answer in Markdown.

Include these sections:

# 📌 Overview

Provide a short overview of the paper.

# 🎯 Research Problem

What problem is being solved?

# ⚙️ Methodology

Explain the proposed approach.

# 📊 Dataset

Mention any datasets used.

# 🏆 Key Findings

List the important findings.

# ⚠️ Limitations

Mention limitations of the work.

# 🚀 Future Work

Suggest future improvements.

Paper:

{text[:15000]}
"""

    return generate(prompt)


# =====================================================
# EXPLAIN SIMPLY
# =====================================================

def explain_simple(text):

    prompt = f"""
Explain this research paper as if you are teaching a high-school student.

Use very simple English.

Include:

## What is the problem?

## How does it work?

## Why is it useful?

## Real-world example

Paper:

{text[:12000]}
"""

    return generate(prompt)


# =====================================================
# KEY TAKEAWAYS
# =====================================================

def key_takeaways(text):

    prompt = f"""
Read the following research paper.

Return ONLY:

# ⭐ Top 5 Key Takeaways

# 🔑 Important Keywords

# 🤖 Models / Algorithms Used

# 📊 Dataset Used

# 📈 Practical Applications

Paper:

{text[:12000]}
"""

    return generate(prompt)


# =====================================================
# QUESTION ANSWERING
# =====================================================

def answer_question(context, question):

    prompt = f"""
You are an AI Research Assistant.

Answer ONLY using the context below.

If the answer is not present, reply exactly:

"I couldn't find that information in the uploaded paper."

Context:

{context}

Question:

{question}
"""

    return generate(prompt)


# =====================================================
# COMPARE TWO PAPERS
# =====================================================

def compare_papers(text1, text2):

    prompt = f"""
Compare these two research papers.

Return your answer in Markdown.

# 📌 Overview

# 🎯 Research Problem

Compare both papers.

# ⚙️ Methodology

Compare the approaches.

# 📊 Dataset

Compare datasets.

# 🏆 Strengths

Paper 1 strengths

Paper 2 strengths

# ⚠️ Weaknesses

Paper 1 weaknesses

Paper 2 weaknesses

# 🥇 Which paper is better?

Give your opinion with reasons.

------------------------

PAPER 1

{text1[:8000]}

------------------------

PAPER 2

{text2[:8000]}
"""

    return generate(prompt)