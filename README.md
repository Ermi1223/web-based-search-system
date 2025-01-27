# Web-Based Search System

This is a web-based search system built with **Streamlit** that allows users to upload **PDF** or **DOCX** files and perform search queries to find the most relevant results. The search is based on **TF-IDF** (Term Frequency - Inverse Document Frequency) and **Cosine Similarity**.

## Features

- Upload PDF and DOCX files.
- Perform search queries and retrieve the most relevant results based on similarity.
- View short snippets of the documents containing the search query.
- Highlight matching terms in the results.
- Display full text of the document with highlighted search terms.

## Installation

To run this project locally, follow the steps below.

### 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/username/repository-name.git
```

### 2. Install required dependencies

Navigate to the project directory:

```bash
cd repository-name
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

Install the required dependencies using **pip**:

```bash
pip install -r requirements.txt
```

### 3. Install additional dependencies (if needed)

If **requirements.txt** doesn't contain some dependencies like `streamlit`, `PyPDF2`, `docx`, or `scikit-learn`, you can manually install them using:

```bash
pip install streamlit PyPDF2 python-docx scikit-learn
```

## Usage

1. Run the Streamlit application:

```bash
streamlit run app.py
```

2. The app will open in your default web browser.
3. Upload your PDF or DOCX files using the file uploader.
4. Enter a search query in the provided input field.
5. The top results will be displayed along with their relevance scores, highlighting matching terms.

## File Upload Types

- **PDF**: Upload PDF files.
- **DOCX**: Upload DOCX files.

## Code Explanation

### File Processing

- PDF files are processed using the **PyPDF2** library.
- DOCX files are processed using the **python-docx** library.
  
### Search and Ranking

The **TF-IDF** vectorizer is used to convert the text into a numerical representation, and **Cosine Similarity** is calculated between the query and documents to rank their relevance.

### Highlights

Matching terms from the search query are highlighted in the text snippets for better visibility.

