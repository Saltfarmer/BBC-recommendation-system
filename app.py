import streamlit as st
import pandas as pd
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")
df = pd.read_csv('BBC_metadata.csv')

st.title("BBC News recommendation system (content based)")

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

# Showing random news
rand = random.randint(0, len(df))

with cover:
  # display the image
  st.image(df['image'].iloc[rand])

with info:
  # display the book information
  st.title(df['title'].iloc[rand])
  st.markdown(df['description'].iloc[rand])
  st.markdown(df['url'].iloc[rand])
  st.markdown(df['keywords'].iloc[rand])  

# Clustering
cluster = st.slider("Choose number of clusters", 2, 10)

list_description = df['description'].tolist()

# filter non-string plots 
list_description = [description for description in list_description if type(description) == str] 

def preprocess(text):
    return text.translate(str.maketrans('', '', string.punctuation))

tfidf_vectorizer = TfidfVectorizer(preprocessor=preprocess, lowercase=True, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(list_description)
kmeans = KMeans(n_clusters=cluster).fit(tfidf)
df['cluster'] = kmeans.labels_

st.dataframe(df.head(10))

# Showing recommendation according to random same cluster
columns = st.columns(5)

for i in range(5):
    with columns[i]:
        st.header(df['title'].iloc[rand])
        st.image(df['image'].iloc[rand])
        

