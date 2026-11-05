import streamlit as st
from openai import OpenAI

# 1. Add a title to the web page
st.title("MY Document Q&A")
st.write("Upload a .txt document and ask a question about it.")

# 2. Ask for the user's OpenAI API key.
#    type="password" hides what is typed. The key is only kept in memory
#    while the page runs. It is never saved, printed, or written to a file.
api_key = st.text_input("OpenAI API key", type="password")

# 3. Let the user upload a .txt document
uploaded_file = st.file_uploader("Upload a document (.txt)", type="txt")

# 4. Let the user type a question about the document
question = st.text_input(
    "Ask a question about the document",
    placeholder="For example: What is this document about?",
)

# 5. Only continue once we have everything we need
if not api_key:
    st.info("Enter your OpenAI API key to continue.")
elif not uploaded_file:
    st.info("Upload a .txt document to continue.")
elif not question:
    st.info("Type a question to continue.")
else:
    # Read the uploaded file and turn its bytes into text
    document = uploaded_file.read().decode("utf-8", errors="ignore")

    # Build the message we send to OpenAI: the document plus the question
    prompt = f"Here is a document:\n\n{document}\n\nQuestion: {question}"

    # 6. Send the document and question to OpenAI
    client = OpenAI(api_key=api_key)
    try:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Answer the question using only the document provided.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        # 7. Display the answer
        st.subheader("Answer")
        st.write(response.choices[0].message.content)
    except Exception as error:
        st.error(f"Something went wrong talking to OpenAI: {error}")
