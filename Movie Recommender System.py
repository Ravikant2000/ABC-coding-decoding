#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


credits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.read_csv('tmdb_5000_movies.csv')


# In[3]:


credits.head(1)['cast']


# In[4]:


movies.head(1)


# In[5]:


movies = movies.merge(credits,on='title')


# In[6]:


movies.head(1)


# In[7]:


# genres
# id
# keywords
# title
# overview
# cast
# crew
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[8]:


movies.head(1)


# In[9]:


movies.isnull().sum()


# In[10]:


movies.dropna(inplace=True)


# In[11]:


movies.duplicated().sum()


# In[12]:


movies.iloc[0].genres


# In[13]:


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


# In[14]:


import ast
ast.literal_eval(movies.iloc[0].genres)


# In[15]:


movies['genres'].apply(convert)


# In[16]:


movies['genres'] = movies['genres'].apply(convert)


# In[17]:


movies.head(1)


# In[18]:


movies['keywords'] = movies['keywords'].apply(convert)


# In[19]:


movies.head(1)


# In[20]:


def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L


# In[21]:


movies['cast'] = movies['cast'].apply(convert3)


# In[22]:


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L


# In[23]:


movies['crew'].apply(fetch_director)


# In[24]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[25]:


movies.head()


# In[26]:


movies['overview'].apply(lambda x: x.split())


# In[27]:


movies['overview'] = movies['overview'].apply(lambda x: x.split())


# In[28]:


movies.head()


# In[29]:


movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])


# In[30]:


movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


# In[31]:


movies.head(1)


# In[32]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[33]:


new_df = movies[['movie_id','title','tags']]
new_df['tags'].apply(lambda x:" ".join(x))


# In[34]:


new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))


# In[35]:


new_df.head()


# In[36]:


import nltk


# In[1]:


from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[38]:


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
        
    return " ".join(y)


# In[39]:


new_df['tags'].apply(stem)
new_df['tags'] = new_df['tags'].apply(stem)


# In[40]:


new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())


# In[41]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')


# In[42]:


cv.fit_transform(new_df['tags']).toarray().shape


# In[43]:


vectors = cv.fit_transform(new_df['tags']).toarray()


# In[44]:


vectors[0]


# In[46]:


cv.get_feature_names_out()


# In[47]:


from sklearn.metrics.pairwise import cosine_similarity


# In[51]:


similarity = cosine_similarity(vectors)


# In[58]:


sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]


# In[62]:


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        print(new_df.iloc[i[0]].title)
    


# In[64]:


recommend('Batman Begins')


# In[65]:


import pickle


# In[67]:


pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))


# In[68]:


with open('movie_dict.pkl', 'rb') as p_f:
    data = pickle.load(p_f)


# In[69]:


data


# In[70]:


pickle.dump(similarity,open('similarity.pkl','wb'))


# In[ ]:




