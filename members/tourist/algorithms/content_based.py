import numpy as np
import pandas as pd
from members.models import Activity
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#load dataset
bhutan=pd.read_csv("members\\tourist\\datasets\\bhutan.csv")
india=pd.read_csv('members\\tourist\\datasets\\india_places.csv')
indonesia=pd.read_csv('members\\tourist\\datasets\\indonesia.csv')

#merg three countries
df = pd.concat([india,bhutan,indonesia],ignore_index = True)
original_df = pd.concat([india,bhutan,indonesia],ignore_index = True)

#removing morphological affixes
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)  
df['about']=df['about'].apply(stem)  

#transform a place description into a vector on the basis of the frequency (count) of each word that occurs in the entire text
cv= CountVectorizer(max_features=5000,stop_words='english')
array=cv.fit_transform(df['about']).toarray()

similar=cosine_similarity(array)

def recommend(place):
    place_index=df[df['item']==place].index[0]
    distances=similar[place_index]
    place_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_Place_list=[]
    recommend_Place_list.append(place)
    for i in place_list:
        recommend_Place_list.append(df.iloc[i[0]]['item'])
    return recommend_Place_list

#function to get searched place     
def master_item(rec_list):
    place_view=rec_list[0]
    masterItem=original_df.loc[original_df['item'] == place_view]
    return masterItem

 
#function to recommend top 5 related places
def recomend_item(rc):
    recommend_list=rc[1:6]
    recomendItem=original_df.loc[original_df['item'].isin(recommend_list)]  
    return recomendItem

#function to give random places
def random_item():
    randomItem=df.sample(n=5)
    return randomItem

#function to give All places
def all_places():
    allItem=list(df['item'])
    return allItem
    

