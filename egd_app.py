import streamlit as st
import openai
import PyPDF2

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Streamlit UI setup
st.set_page_config(page_title="EGD Genius", page_icon="📐")
st.title("📐 EGD Genius: Your AI Design Buddy")

# Topic selector for EGD subjects
topic = st.selectbox("Choose a topic", [
    "Isometric Drawing",
    "Orthographic Projection",
    "Design Process",
    "CAD Theory",
    "Dimensioning & Scale"
])

# Question input
question = st.text_area("Ask your EGD question")

# Response button
if st.button("Get Help") and question.strip():
    with st.spinner("Sketching out ideas..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful tutor for EGD students, specializing in {topic}."},
                    {"role": "user", "content": f"Explain this in simple terms: {question}"}
                ]
            )
            st.markdown("### 🧾 Answer")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# PDF upload section
uploaded_file = st.file_uploader("Upload your drawing or notes (PDF)")
if uploaded_file:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        st.success("Notes uploaded successfully!")
        st.markdown("### 📄 Extracted Content")
        st.write(text)
    except Exception as e:
        st.error(f"Could not read PDF: {e}")
