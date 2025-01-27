import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re
import docx
from PyPDF2 import PdfReader

# Define custom stop words
stop_words = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
    'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
    'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
    'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn',
    'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn',
    'wasn', 'weren', 'won', 'wouldn'
]

def process_documents(uploaded_files):
    """Extract text from uploaded files."""
    documents = []
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""  # Handling empty or unreadable text
            documents.append(text)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            text = " ".join([p.text for p in doc.paragraphs])
            documents.append(text)
    return documents

def highlight_query(text, query):
    """Highlight the query terms in the result snippet."""
    pattern = re.compile(f"({re.escape(query)})", re.IGNORECASE)
    highlighted_text = pattern.sub(r"**\1**", text)
    return highlighted_text

def search_documents(query, documents, top_n):
    """Perform search and return top N results."""
    vectorizer = TfidfVectorizer(
        stop_words=stop_words,
        max_df=1.0,
        min_df=0.001,
        max_features=1000  # Limit the number of features to improve vectorization
    )
    try:
        X = vectorizer.fit_transform(documents)
    except ValueError as e:
        st.error(f"Error processing documents: {e}")
        return []
    
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, X).flatten()

    # Log similarities to debug
    st.write(f"Cosine Similarity Scores: {similarities}")
    
    results = sorted(
        [(i, documents[i], similarities[i]) for i in range(len(documents))],
        key=lambda x: x[2],
        reverse=True
    )
    return results[:top_n]  # Ensure this is sliced based on the selected top_n value

def clean_text(text):
    """Remove unwanted characters and clean up the text."""
    text = re.sub(r"\\[a-z]+", "", text)  # Remove LaTeX-like commands
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove all non-alphanumeric characters except spaces
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace
    return text.strip()

def main():
    st.title("Web-Based Search System")
    st.markdown("Upload PDF or DOCX files and perform a search query to find the most relevant results.")

    uploaded_files = st.file_uploader(
        "Upload your files",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        documents = process_documents(uploaded_files)
        if not documents:
            st.warning("No text extracted from the uploaded documents.")
        else:
            st.success(f"Uploaded {len(documents)} documents successfully!")

        query = st.text_input("Enter your search query:")
        top_n = st.slider("Number of top results to display:", min_value=1, max_value=10, value=5)

        if st.button("Search"):
            if query.strip():
                results = search_documents(query, documents, top_n)
                st.subheader(f"Top {top_n} results for your query '{query}':")
                if results:
                    for i, (index, content, score) in enumerate(results, start=1):
                        st.markdown(f"### Result {i}")
                        st.write(f"**Relevance Score:** {score:.4f}")
                        snippet = clean_text(content[:800])  # Display the first 800 characters for better context
                        highlighted_snippet = highlight_query(snippet, query)
                        st.markdown(highlighted_snippet)

                        with st.expander("View Full Document"):
                            full_text = clean_text(content)
                            highlighted_full_text = highlight_query(full_text, query)
                            st.markdown(highlighted_full_text)
                else:
                    st.warning("No relevant results found. Try adjusting your query.")
            else:
                st.error("Please enter a search query.")

if __name__ == "__main__":
    main()
