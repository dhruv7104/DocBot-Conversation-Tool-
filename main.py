import streamlit as st
import fitz  # PyMuPDF
import spacy
import json
from io import BytesIO  

nlp = spacy.load("en_core_web_sm")

def app():
    # Q&A history
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    # Function to extract text from PDF
    def extract_text_from_pdf(uploaded_pdf):
        text_content = ""
        pdf = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text_content += page.get_text() + "\n" 
        return text_content

    # Function to generate a summary of the PDF content
    def summarize_text(pdf_text):
        doc = nlp(pdf_text)
        sentences = [sent.text for sent in doc.sents]
        summary = " ".join(sentences[:10])  
        return summary

    # Function to answer questions based on PDF content
    def answer_question(pdf_text, question):
        if "summary" in question.lower():  
            return summarize_text(pdf_text)
        
        # Analyze question for keywords and context
        doc_question = nlp(question)
        keywords = [token.lemma_ for token in doc_question if not token.is_stop and token.pos_ in {"NOUN", "PROPN", "ADJ"}]
        
        # Generate answer by matching keywords in PDF text
        answer = ""
        found_sentences = []
        for sentence in pdf_text.split("."):
            if all(keyword in sentence.lower() for keyword in keywords):
                found_sentences.append(sentence.strip())
        
        # Format answer
        answer = " ".join(found_sentences[:5])
        if not answer:
            answer = "I'm sorry, I couldn't find an answer in the PDF."
        
        return answer

    # Streamlit UI
    st.title("DocBot Tool")

    uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_pdf:
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        
        if st.checkbox("Show PDF content"):
            st.text_area("Extracted PDF Content", pdf_text, height=300)
        
        user_question = st.text_input("Ask a question about the PDF:")
        
        if user_question:
            answer = answer_question(pdf_text, user_question)
            st.session_state.qa_history.append({"question": user_question, "answer": answer})
            st.write("**Answer:**", answer)
        
        if st.session_state.qa_history:
            st.write("### Previous Q&A")
            for i, entry in enumerate(st.session_state.qa_history, 1):
                st.write(f"**Q{i}:** {entry['question']}")
                st.write(f"**A{i}:** {entry['answer']}")
        
        # if st.button("Save PDF content as JSON"):
        #     with open("extracted_pdf_content.json", "w") as f:
        #         json.dump({"content": pdf_text}, f)
        #     st.write("PDF text saved to extracted_pdf_content.json")


if __name__ == "__main__":
    app()
