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

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

# Choosing random default key in state session
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
  st.markdown("# [Watch It](" + df['url'].iloc[key] + ")", unsafe_allow_html=True)
  st.caption("Keywords : " + df['keywords'].iloc[key])

# Clustering 
st.title("How does it works ? ")
st.markdown("The systems works by randomly recommending based on clustering with K-Means and the specific category that user choose. The idea of k-means is that we assume there are k groups in our dataset. We then try to group the data into those k groups. Each group is described by a single point known as a centroid. The centroid of a cluster is the mean value of the points within the cluster. In this case as a user, you are free to choose the number of `k` cluster. Later on the system will consider your input on the number of cluster and category to create recommendations.")

# Clustering process
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

# Showing recommendation according to random same cluster
sample1 = df[df['cluster'] == df['cluster'].iloc[key]].sample(n=5)

st.title("5 Recommendation based on description cluster and random category")
columns = st.columns(5)

def keychanger(keymaker):
  st.session_state['key'] = keymaker

for i in range(5):
    with columns[i]:
      keymaker = df[df['title'] == sample1['title'].iloc[i]].index.tolist()[0]
      st.button(sample1['title'].iloc[i], on_click=keychanger, args=(keymaker, ))
      st.image(sample1['image'].iloc[i])

st.title("5 Recommendation based on description cluster and category")
# Let user choose the category
choice = st.selectbox("Choose the category", df['category'].unique().tolist(), index=df['category'].unique().tolist().index(df['category'].iloc[key]))

# Showing recommendation according to random same cluster and category
sample2 = df[(df['cluster'] == df['cluster'].iloc[key]) & (df['category'] == choice)].sample(n=5)

columns = st.columns(5)

for i in range(5):
    with columns[i]:
      keymaker = df[df['title'] == sample2['title'].iloc[i]].index.tolist()[0]
      st.button(sample2['title'].iloc[i], on_click=keychanger, args=(keymaker, ))
      st.image(sample2['image'].iloc[i])