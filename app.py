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
st.image("https://ichef.bbci.co.uk/images/ic/1920x1080/p09xtmrp.jpg")

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

rand = random.randint(0, len(df))

with cover:
  # display the image
  st.image(df['image'].iloc[rand])

with info:
  # display the book information
  st.header(df['title'].iloc[rand])
  st.markdown(df['description'].iloc[rand])  
  st.markdown("Keywords : " + df['keywords'].iloc[rand])
  if st.button("Watch"):
    st.markdown(df['url'].iloc[rand])

# Clustering
st.title("What is K-means")
st.markdown("k-means clustering is a method of vector quantization, originally from signal processing, that aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean (cluster centers or cluster centroid), serving as a prototype of the cluster. This results in a partitioning of the data space into Voronoi cells. k-means clustering minimizes within-cluster variances (squared Euclidean distances), but not regular Euclidean distances, which would be the more difficult Weber problem: the mean optimizes squared errors, whereas only the geometric median minimizes Euclidean distances. For instance, better Euclidean solutions can be found using k-medians and k-medoids. ")

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
sample = df[(df['cluster'] == df['cluster'].iloc[rand]) & (df['category'] == choice)].sample(n=5)

columns = st.columns(5)

for i in range(5):
    with columns[i]:
        if st.button(sample['title'].iloc[i]):
          st.session_state['idx'] = df[df['title'] == sample['title'].iloc[i]].index.tolist()[0]
        st.image(sample['image'].iloc[i])
        

