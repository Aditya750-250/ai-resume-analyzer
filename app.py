import streamlit as st
import PyPDF2
import google.generativeai as genai

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# Configure API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

st.markdown("""
<h1 style='text-align: center;'>📄 AI Resume Analyzer</h1>
<p style='text-align: center; color: gray;'>
Analyze resumes using Gemini AI
</p>
""", unsafe_allow_html=True)
with st.sidebar:
    st.header("About")
    st.write("""
    This AI-powered app analyzes resumes and provides:

    - ATS Score
    - Skill Suggestions
    - Resume Improvements
    - Career Feedback
    """)

with st.container():

    st.subheader("📤 Upload Your Resume")

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )
if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    st.success("Resume Uploaded Successfully!")

    if st.button("Analyze Resume"):

        prompt = f"""
        You are an expert ATS resume reviewer.

        Analyze this resume professionally.

        Return your response in this format:

        ATS Score: number/100

        Strengths:
        - bullet points

        Weaknesses:
        - bullet points

        Missing Skills:
        - bullet points

        ATS Optimization Tips:
        - bullet points

        Final Recommendation:
        - short paragraph

        Resume:
        {text}
        """

        with st.spinner("Analyzing Resume..."):

            try:
                response = model.generate_content(prompt)

                st.subheader("AI Feedback")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("Built with Python, Streamlit, and Gemini AI")