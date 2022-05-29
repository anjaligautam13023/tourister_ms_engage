#this code is combination of content based and collaborative filtering
#it solves cold start problem

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from members.models import Activity
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

bhutan=pd.read_csv("members/tourist/datasets/bhutan.csv")
india=pd.read_csv('members/tourist/datasets/india_places.csv')
indonesia=pd.read_csv('members/tourist/datasets/indonesia.csv')

#merging three dataset 
df = pd.concat([india,bhutan,indonesia],ignore_index = True)
original_df = pd.concat([india,bhutan,indonesia],ignore_index = True)

#removing morphological affixes
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)    

#applying PorterStemmer to description of function
df['about']=df['about'].apply(stem)



#converts description in text to numbers 
tfidf=TfidfVectorizer(stop_words='english')
tfidf_matrix=tfidf.fit_transform(df['about'])
tfidf_df=pd.DataFrame(tfidf_matrix.toarray(), index=df.index.tolist())


svd=TruncatedSVD(n_components =10)
latent_matrix=svd.fit_transform(tfidf_df)

n=10
latent_matrix_1_df=pd.DataFrame(latent_matrix[:,0:n], index=df.item.tolist())

#loads user activities from database
rating = Activity().activity_dataframe()


user_df = pd.merge(rating,df, on='item')
user_df=user_df.dropna(axis=0, subset=['item'])
ratingcount=(user_df.groupby(by=['item'])['rate'].count().reset_index().rename(columns={'rate':'totalrating'})[['item','totalrating']])
rating_count= pd.merge(user_df,ratingcount,on='item')


#drop duplicates and creates a pivot table
r=rating_count.drop_duplicates(['user_id','item'])
rating_new2=r.pivot(index='item',columns='user_id',values='rate').fillna(0)



svd=TruncatedSVD(n_components=10)
latent_matrix_2=svd.fit_transform(rating_new2)
latent_matrix_2_df=pd.DataFrame(latent_matrix_2,index=ratingcount.item.tolist())

#function which returns recommended place by content based filtering and collaborative filtering
def hybrid_recommendation(place):
   
    a_1=np.array(latent_matrix_1_df.loc[place]).reshape(1,-1)
    a_2=np.array(latent_matrix_2_df.loc[place]).reshape(1,-1)

    ascore_1=cosine_similarity(latent_matrix_1_df,a_1).reshape(-1)
    ascore_2=cosine_similarity(latent_matrix_2_df,a_2).reshape(-1)

    x=abs(ascore_2.size-ascore_1.size)
    con = np.concatenate((ascore_2, np.zeros(x)))
    hybrid=((ascore_1+con)/2.0)

    dictdf={'content': ascore_1 , 'collaborative' : con, 'hybrid':hybrid}
    similar=pd.DataFrame(dictdf,index=latent_matrix_1_df.index)

    similar.sort_values('hybrid',ascending=False ,inplace=True)
    rp=original_df.loc[original_df['item'].isin(list(similar.index)[1:10])] 
    return rp   