import streamlit as st
from transformers import pipeline

# get content from - https://www.toppr.com/guides/english-language/reading-comprehension/paragraph-based-questions/#Paragraph_Contents

# Load the question answering pipeline from Hugging Face
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased")

def answer_question(context, question):
    result = qa_pipeline(context=context, question=question)
    return result['answer']

def main():
    st.title("Document Question Answering Web App")

    # Add a textarea for user to input the document context
    context = st.text_area("Enter the document context:", "")

    # Add a text input for user to input the question
    question = st.text_input("Enter your question:", "")

    if st.button("Answer"):
        if context and question:
            answer = answer_question(context, question)
            st.write("Answer:")
            st.write(answer)
        else:
            st.warning("Please provide both document context and question.")

if __name__ == "__main__":
    main()
