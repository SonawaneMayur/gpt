import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = "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"

# Define available engines
engines = [
"gpt-3.5-turbo-0613",
    "text-davinci-003",
    "text-davinci-002",
    "text-davinci-001",
    # Add more engines as needed
]

# def generate_response(prompt, engine):
#     response = openai.Completion.create(
#         engine=engine,
#         prompt=prompt,
#         max_tokens=100  # Adjust the length of the generated response
#     )
#     return response.choices[0].text
#
# def main():
#     st.title("LLM Web App")
#
#     # Add the dropdown menu to the sidebar
#     selected_engine = st.sidebar.selectbox("Select an Engine", engines)
#
#     # Add a text input for user input
#     user_input = st.text_input("Enter your prompt:", "")
#
#     if st.button("Generate"):
#         if user_input:
#             response = generate_response(user_input, selected_engine)
#             st.write("Generated Response:")
#             st.write(response)
#         else:
#             st.warning("Please enter a prompt.")
#
# if __name__ == "__main__":
#     main()


# Define available engines
engines = [
    "text-davinci-003",
    "text-davinci-002",
    "text-davinci-001",
    # Add more engines as needed
]

def generate_response(prompt, engine):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=100  # Adjust the length of the generated response
    )
    return response.choices[0].text

def compare_responses(prompt, selected_engine):
    comparisons = []
    for engine in engines:
        if engine != selected_engine:
            comparison_response = generate_response(prompt, engine)
            comparisons.append((engine, comparison_response))
    return comparisons

def main():
    st.title("GPT-3 Comparison Web App")

    # Add a text input for user input
    user_input = st.text_input("Enter your prompt:", "")

    # Position the select box on the right corner using CSS
    st.write(
        f'<style>.css-1vyn35r{{float:right;}}</style>',
        unsafe_allow_html=True
    )
    selected_engine = st.selectbox("Select an Engine", engines)

    if st.button("Generate"):
        if user_input:
            response = generate_response(user_input, selected_engine)
            st.write("Generated Response:")
            st.write(response)
            compare_link = f'<a href="#comparison">Compare with Other Engines</a>'
            st.markdown(compare_link, unsafe_allow_html=True)
        else:
            st.warning("Please enter a prompt.")

    # Add a separator
    st.markdown("---")

    # Comparison section
    if st.button("Compare"):
        if user_input:
            comparisons = compare_responses(user_input, selected_engine)
            st.markdown("<h2 id='comparison'>Comparison with Other Engines</h2>", unsafe_allow_html=True)
            for engine, comparison_response in comparisons:
                st.write(f"**{engine} Output:**")
                st.write(comparison_response)
                st.markdown("---")

if __name__ == "__main__":
    main()
