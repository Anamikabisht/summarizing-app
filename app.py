
import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Title
st.title("📝 Extractive Text Summarizer")
st.write("This app summarizes your input text using basic NLP techniques.")

# Text Input
text = st.text_area("Enter the text to summarize:", height=300)

if st.button("Generate Summary"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        doc = nlp(text)
        stopwords = list(STOP_WORDS)
        allowed_pos = ['ADJ', 'PROPN', 'VERB', 'NOUN']

        # Token filtering
        tokens = []
        for token in doc:
            if token.text.lower() in stopwords or token.text in punctuation:
                continue
            if token.pos_ in allowed_pos:
                tokens.append(token.text.lower())

        # Word frequency
        word_freq = Counter(tokens)

        # Sentence scoring
        sentence_scores = {}
        for sent in doc.sents:
            for word in sent:
                word_lower = word.text.lower()
                if word_lower in word_freq:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word_lower]

        # Get top 2 sentences
        top_sentences = nlargest(2, sentence_scores, key=sentence_scores.get)
        summary = ' '.join([sent.text for sent in top_sentences])

        # Output
        st.subheader("📌 Summary:")
        st.write(summary)
