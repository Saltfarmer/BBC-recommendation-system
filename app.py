import streamlit as st
import pandas as pd
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

st.set_page_config(layout="wide")

df = pd.read_csv('BBC_metadata.csv')

st.title("Where the recommendation came from ?")
st.markdown("The data is gathered from [BBC](https://www.bbc.co.uk/iplayer). gather all of the metadata that might be useful for my recommendation system. Starting from the `Title`, `Description`, `Images`, `Url`, `Category`, and `Keywords`. I am using the `BeautifulSoup4` library to get all metadata from all the articles that have been gathered or provided before. Then I save all the metadata from all articles to process it later as a recommendation system later as a Comma Separable Value files. Here is the example of what the metadata looks like.")
st.dataframe(df.sample(5))
st.markdown("So here as a starting point, recommendation system will provide you with completely random recommendation based on all available data")
st.title("Random recommendation")

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
st.title("Recommendation with clustering")
st.header("How does it works ? ")
st.markdown("The systems works by randomly recommending based on clustering with K-Means and the specific category that user choose. The idea of k-means is that we assume there are k groups in our dataset. We then try to group the data into those k groups. Each group is described by a single point known as a centroid. The centroid of a cluster is the mean value of the points within the cluster. In this case as a user, you are free to choose the number of `k` cluster. The user can choose the number of cluster depends on how many cluster would be in all of the contents of BBC. Later on the system will consider your input on the number of cluster and category to create recommendations.")

# Clustering process
cluster = st.slider("Choose number of clusters", 2, 10, value=5)

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

st.dataframe(df[['title', 'description', 'cluster']].sample(n=5))
st.markdown("Then you can choose the detail of the 5 recommendation of the same cluster of starting point recommendation")

st.title("5 Recommendation based on description cluster and random category")
columns = st.columns(5)

def keychanger(keymaker):
  st.session_state['key'] = keymaker

for i in range(5):
    with columns[i]:
      keymaker = df[df['title'] == sample1['title'].iloc[i]].index.tolist()[0]
      st.button(sample1['title'].iloc[i], on_click=keychanger, args=(keymaker, ))
      st.markdown(sample1['category'].iloc[i])
      st.image(sample1['image'].iloc[i])

st.title("5 Recommendation based on description cluster and category")
# Let user choose the category
st.markdown("You can also choose of some specific category that you want.")
choice = st.selectbox("Choose the category", df['category'].unique().tolist(), index=df['category'].unique().tolist().index(df['category'].iloc[key]))

# Showing recommendation according to random same cluster and category
sample2 = df[(df['cluster'] == df['cluster'].iloc[key]) & (df['category'] == choice)].sample(n=5)

columns = st.columns(5)

for i in range(5):
    with columns[i]:
      keymaker = df[df['title'] == sample2['title'].iloc[i]].index.tolist()[0]
      st.button(sample2['title'].iloc[i], on_click=keychanger, args=(keymaker, ))
      st.image(sample2['image'].iloc[i])