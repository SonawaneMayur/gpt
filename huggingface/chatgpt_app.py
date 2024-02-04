import streamlit as st
from transformers import pipeline

# Load the text generation pipeline from Hugging Face
text_generator = pipeline("text-generation", model="gpt2")

def generate_text(prompt, max_length=50):
    generated_text = text_generator(prompt, max_length=max_length)[0]["generated_text"]
    return generated_text

def main():
    st.title("Hugging Face Transformers Web App")

    # Add a text input for user input
    user_input = st.text_input("Enter your prompt:", "")

    if st.button("Generate"):
        if user_input:
            generated_text = generate_text(user_input)
            st.write("Generated Text:")
            st.write(generated_text)
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()
