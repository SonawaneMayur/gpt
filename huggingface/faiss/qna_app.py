import streamlit as st
import torch
from transformers import pipeline, AutoModel, AutoTokenizer
import faiss
import numpy as np

# Load the question answering pipeline from Hugging Face
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", tokenizer="distilbert-base-cased")

# Load a pre-trained model and tokenizer for embedding generation
embedding_model_name = "distilbert-base-cased"
embedding_model = AutoModel.from_pretrained(embedding_model_name)
embedding_tokenizer = AutoTokenizer.from_pretrained(embedding_model_name)

# Create a vector index for Faiss
index = faiss.IndexFlatL2(768)  # Assuming the embeddings are of size 768

def generate_text_embedding(text):
    encoded_input = embedding_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        model_output = embedding_model(**encoded_input)
        text_embedding = model_output.last_hidden_state.mean(dim=1)  # Mean pooling for sentence-level embedding
    return text_embedding.numpy()

def add_to_vector_db(text_embedding):
    index.add(np.array(text_embedding))

def context_search(query_embedding):
    _, indices = index.search(query_embedding, 1)
    return indices[0][0]

def similarity_search(query_embedding, top_k=3):
    _, indices = index.search(query_embedding, top_k)
    return indices[0]

def answer_question(context, question):
    result = qa_pipeline(context=context, question=question)
    return result['answer']

def main():
    st.title("Document Question Answering and Embedding Search Web App")

    # Add a textarea for user to input the document context
    context = st.text_area("Enter the document context:", "")

    # Add a text input for user to input the question
    question = st.text_input("Enter your question:", "")

    if st.button("Answer"):
        if context and question:
            answer = answer_question(context, question)
            st.write("Answer:")
            st.write(answer)

            # Generate embedding for the provided context
            context_embedding = generate_text_embedding(context)
            st.write("Context Embedding:")
            st.write(context_embedding)  # Display embedding (replace with desired display format)

            # Add context embedding to the vector database
            add_to_vector_db(context_embedding)
        else:
            st.warning("Please provide both document context and question.")

        if st.button("Search Similar"):
            # Perform similarity search using context embedding
            similar_document_indices = similarity_search(context_embedding)
            st.write("Similar Document Indices:")
            st.write(similar_document_indices)

if __name__ == "__main__":
    main()
