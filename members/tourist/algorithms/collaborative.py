#this code is to find the places liked by similar users
#collaborative filtering is used

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
from members.models import Activity
import operator

#load dataset
bhutan=pd.read_csv("members\\tourist\\datasets\\bhutan.csv")
india=pd.read_csv('members\\tourist\\datasets\\india_places.csv')
indonesia=pd.read_csv('members\\tourist\\datasets\\indonesia.csv')

#merg three countries
df = pd.concat([india,bhutan,indonesia],ignore_index = True)

#load user activity from database
user = Activity().activity_dataframe()

user_df = pd.merge(user,df,on='item')
user_df=user_df.dropna(axis=0, subset=['item'])
ratingcount=(user_df.groupby(by=['item'])['rate'].count().reset_index().rename(columns={'rate':'totalrating'})[['item','totalrating']])

total_rating_count=user_df.merge(ratingcount,on='item')
rating=total_rating_count.drop_duplicates(['user_id','item'])

#create pivot table
pivot=rating.pivot(index='user_id',columns='item',values='rate')
rating_matrix = pivot.fillna(0)

#function to find similar users
def similar_users(user_id, matrix, k=5):
    user = matrix[matrix.index == user_id]
    other_users = matrix[matrix.index != user_id]
    similarities = cosine_similarity(user,other_users)[0].tolist()
    indices = other_users.index.tolist()
    index_similarity = dict(zip(indices, similarities))
    index_similarity_sorted = sorted(index_similarity.items(), key=operator.itemgetter(1))
    index_similarity_sorted.reverse()
    top_users_similarities = index_similarity_sorted[:k]
    users = [u[0] for u in top_users_similarities]
    return users
  
#function to recommend similar item using using users
def recommend_item(user_index, similar_user_indices, matrix, items=11):
    similar_users = matrix[matrix.index.isin(similar_user_indices)]
    similar_users = similar_users.mean(axis=0)
    similar_users_df = pd.DataFrame(similar_users, columns=['mean'])
    user_df = matrix[matrix.index == user_index]
    user_df_transposed = user_df.transpose()
    user_df_transposed.columns = ['rate']
    user_df_transposed = user_df_transposed[user_df_transposed['rate']==0]
    places_unseen = user_df_transposed.index.tolist()
    similar_users_df_filtered = similar_users_df[similar_users_df.index.isin(places_unseen)]
    similar_users_df_ordered = similar_users_df.sort_values(by=['mean'], ascending=False)
    top_n_place = similar_users_df_ordered.head(items)
    top_n_place_indices = top_n_place.index.tolist()
    place_information = rating[rating['item'].isin(top_n_place_indices)]
    return  place_information.drop_duplicates(['item'])    

#function to call in view to return places
def collaborative_item(id):
    similar_user_indices = similar_users(id, rating_matrix)
    collaborativeItems=recommend_item(id, similar_user_indices, rating_matrix)
    return collaborativeItems
      








































