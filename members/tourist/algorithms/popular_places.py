#this is code is to find popular places 
#popular places are find using weighted-average score

from tokenize import group
import numpy as np
import pandas as pd
from members.models import Activity

#load dataset
bhutan=pd.read_csv('members\\tourist\\datasets\\bhutan.csv')
indonesia=pd.read_csv("members\\tourist\\datasets\\indonesia.csv")
india=pd.read_csv('members\\tourist\\datasets\\india_places.csv')
df = pd.concat([india,bhutan,indonesia],ignore_index = True)

#load user activities from database
user = Activity().activity_dataframe()

z=user['clicks'].sum()
avclick= user.groupby(by="item",as_index=False)['clicks'].sum()
avclick['clicks']=avclick['clicks']*(5/z)
Mean = user.groupby(by="item",as_index=False)['rate'].mean()
group_user=user.groupby(by="item",as_index=False)['user_id'].count()

#w=weighted rating
#r=average rating for place
#v=no of rating for movies
#m=minimum votes required
#c=mean rating across whole rating

y=pd.merge(Mean,group_user, on='item')
v=y['user_id']
r=y['rate']+avclick['clicks']
c=r.mean()
m=y['user_id'].quantile(0.70)
y['w']=(((r*v)+(c*m))/(v+m))
place=y.sort_values('w',ascending=False)
x=list(place['item'][1:11])
popularItem=df.loc[df['item'].isin(x)]

#function to return popular items
def popular_item():
    return popularItem


