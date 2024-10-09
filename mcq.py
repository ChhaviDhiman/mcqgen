import streamlit as st
import PyPDF2
import g4f

# Function to read the uploaded file (PDF or text)
def read_file(uploaded_file):
    try:
        if uploaded_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.strip()
        
        elif uploaded_file.name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")
            return text.strip()
        
        else:
            st.error("Unsupported file format! Please upload a PDF or text file.")
            return None
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

# Function to use GPT model (g4f) to generate MCQs
def generate_mcqs_gpt(text, num_mcqs, tone):
    prompt = f"""
    Text: {text}
    
    You are an expert MCQ generator. Create {num_mcqs} multiple-choice questions from the text provided, with options and answers. \
    Make sure the questions match the tone: {tone}.
    
    Format the response as follows:
    Question: <your question here>
    a) <option1>
    b) <option2>
    c) <option3>
    d) <option4>
    Answer: <correct answer>
    """
    
    available_models = dir(g4f.models)
    print("Available models:", available_models)

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,  # Update this line after checking available models
            messages=[{"role": "user", "content": prompt}]
        )

        print("Response from GPT:", response)  # Debugging line to check the response

        # Return the response directly if it's a string
        return response
    except AttributeError as e:
        st.error("Model not found. Please check available models.")
        return None
    except Exception as e:
        st.error(f"Error during MCQ generation: {str(e)}")
        return None


# Streamlit UI
st.title("MCQs Creator Application with LangChain 🦜⛓️")

# File upload
uploaded_file = st.file_uploader("Upload a PDF or Text File", type=["pdf", "txt"])

if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")
    
    # Step 1: Extract text from the file
    text = read_file(uploaded_file)
    
    if text:
        st.write("### File Content:")
        st.write(text[:1000])  # Display first 1000 characters of the file to confirm

        # Input for number of MCQs
        num_mcqs = st.number_input("Number of MCQs", min_value=1, max_value=10, value=5)

        # Tone of the quiz
        tone = st.text_input("Tone of the Questions", value="Academic", placeholder="Simple, Academic, Fun, etc.")
        
        # Generate and display MCQs
        if st.button("Generate MCQs"):
            with st.spinner("Generating MCQs using GPT-4..."):
                mcq_output = generate_mcqs_gpt(text, num_mcqs, tone)
                if mcq_output:
                    st.write("### Generated MCQs:")
                    st.text(mcq_output)
