import streamlit as st
import pandas as pd
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")

df = pd.read_csv('BBC_metadata.csv')

st.title("BBC recommendation system (content based)")

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

rand = random.randint(0, len(df))

with cover:
  # display the image
  st.image(df['image'].iloc[rand])

with info:
  # display the book information
  st.title(df['title'].iloc[rand])
  st.header("Description")
  st.markdown(df['description'].iloc[rand])  
  st.markdown("Keywords : " + df['keywords'].iloc[rand])
  if st.button("Watch"):
    st.markdown(df['url'].iloc[rand])

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

# Let user choose the category
choice = st.selectbox("Choose the category", df['category'].unique().tolist())

# Showing recommendation according to random same cluster
sample = df[(df['cluster'] == df['cluster'].iloc[rand]) & (df['category'] == choice)].sample(n=5)

columns = st.columns(5)

for i in range(5):
    with columns[i]:
        if st.button(sample['title'].iloc[i]):
          st.session_state['idx'] = df[df['title'] == sample['title'].iloc[i]].index.tolist()[0]
        st.image(sample['image'].iloc[i])
        

