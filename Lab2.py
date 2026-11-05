import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# 1. Add a title to the web page
st.title("Lab 2: PDF Summarizer")
st.write("Upload a PDF and get a summary. Pick your options in the sidebar.")

# 2. Get the OpenAI API key from Streamlit secrets.
#    Locally it comes from .streamlit/secrets.toml (which Git ignores).
#    On Streamlit Community Cloud it comes from the app's Settings -> Secrets.
if "OPENAI_API_KEY" not in st.secrets:
    st.error("No OpenAI API key found. Add OPENAI_API_KEY to your Streamlit secrets.")
    st.stop()
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Sidebar dropdown menus
language = st.sidebar.selectbox(
    "Language", ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
)

summary_type = st.sidebar.selectbox(
    "Type of summary",
    [
        "Summarize the document in 100 words",
        "Summarize the document in 2 connecting paragraphs",
        "Summarize the document in 5 bullet points",
    ],
)

# The first model in the list is the default.
models = {
    "Mini (gpt-5-mini): faster and cheaper": "gpt-5-mini",
    "Flagship (gpt-5): higher quality, costs more": "gpt-5",
}
model_label = st.sidebar.selectbox("Model", list(models.keys()))
model = models[model_label]

# 4. Let the user upload a PDF
uploaded_file = st.file_uploader("Upload a document (.pdf)", type="pdf")


# 5. Turn the PDF into plain text, one page at a time
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


# 6. Ask OpenAI for the summary.
#    @st.cache_data remembers each answer, so switching pages or clicking
#    around doesn't pay for the same summary twice. Changing the document,
#    summary type, language, or model asks for a new one.
@st.cache_data(show_spinner=False)
def summarize(document, summary_type, language, model):
    instructions = (
        f"{summary_type}. Write the summary in {language}. "
        "Use only the information in the document."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": f"Here is the document:\n\n{document}"},
        ],
    )
    return response.choices[0].message.content


# 7. As soon as a PDF is uploaded, show the summary (no question needed)
if not uploaded_file:
    st.info("Upload a PDF to see its summary.")
else:
    document = read_pdf(uploaded_file)
    if not document.strip():
        st.warning("Couldn't find any text in this PDF. It may be a scanned image.")
    else:
        try:
            with st.spinner("Summarizing..."):
                summary = summarize(document, summary_type, language, model)
            st.subheader("Summary")
            st.write(summary)
            st.caption(f"Model used: {model}")
        except Exception as error:
            st.error(f"Something went wrong talking to OpenAI: {error}")

# 8. Lab 2d: which model should be the default, and why
with st.expander("Why is the mini model the default?"):
    st.write(
        "Summarizing a document is a fairly easy task, and the mini model "
        "does it well at a much lower cost and faster than the flagship model. "
        "Since every new upload or option change sends the whole document to "
        "OpenAI, the savings add up. Users can still switch to the flagship "
        "model when they need a higher-quality summary, such as for a long or "
        "complicated document."
    )
