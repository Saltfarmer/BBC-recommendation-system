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
st.title("")
# st.image("https://ichef.bbci.co.uk/images/ic/1920x1080/p09xtmrp.jpg")

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

if 'key' not in st.session_state:
  st.session_state['key'] = random.randint(0, len(df))

key = st.session_state['key']

with cover:
  # display the image
  st.image(df['image'].iloc[key])

with info:
  # display the book information
  st.header(df['title'].iloc[key])
  st.markdown(df['description'].iloc[key])  
  st.caption("Keywords : " + df['keywords'].iloc[key])
  st.markdown("# [Watch It](" + df['url'].iloc[key] + ")", unsafe_allow_html=True)

# Clustering
st.title("What is K-means ?")
st.markdown("The idea of k-means is that we assume there are k groups in our dataset. We then try to group the data into those k groups. Each group is described by a single point known as a centroid. The centroid of a cluster is the mean value of the points within the cluster. So as a user, you are free to choose the number of `k` cluster")
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

# st.dataframe(df.head(10))

# Let user choose the category
choice = st.selectbox("Choose the category", df['category'].unique().tolist())

# Showing recommendation according to random same cluster
sample = df[(df['cluster'] == df['cluster'].iloc[key]) & (df['category'] == choice)].sample(n=5)

columns = st.columns(5)

def keychanger(keymaker):
  st.session_state['key'] = keymaker

for i in range(5):
    with columns[i]:
      keymaker = df[df['title'] == sample['title'].iloc[i]].index.tolist()[0]
      st.markdown(keymaker) 
      st.button(sample['title'].iloc[i], on_click=keychanger, args=(keymaker, ))
      st.image(sample['image'].iloc[i])