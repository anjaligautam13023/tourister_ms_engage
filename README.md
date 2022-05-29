# Tourist-Recommender-System(Tourister)
video demo-https://youtu.be/IFeMAE1myHg<br />
website url-https://tourister-msengage.herokuapp.com/index.html

# Objective:
To recommend user places based on content based, collaborative based and hybrid based filteration and also to provide a plan for user consisting of various services

# Project Overview:
I have used 4 algoriths in this project
- when user is not logged in<br />
   1.To show popular places average weighted score is used
   ![msengage7](https://user-images.githubusercontent.com/91557659/170885598-1a8dbfe2-2668-4916-a3a3-99940978cc7d.PNG)

- when user is logged in<br />
   2. collaborative filtering to show places liked by similar users<br />
   3. content based filtering too show similar places<br />
   ![image](https://user-images.githubusercontent.com/91557659/170885555-33f629f1-933f-4f74-ab19-48035cd48f34.png)
   4. hybrid(content-based and collaborative) to solve cold start problem <br />
   ![image](https://user-images.githubusercontent.com/91557659/170885654-2a9f68d6-cd84-4302-b22f-06afc435f15b.png)
   
## Description:
When application is open up it shows you randomly picked places from dataset ,those place can be viewed by clicking on view button. Places can also be searched on searching in search box. When application is opened at first time it will show popular places based on average weighhted score. When user is signed up data is stored to database and at the time of login details are verified from database. Once user is logged in it will show similar places using collaborative filtering.On view of a place recommendation are made which are completely content based based on cosine similarity. You can also see the recommendation below which are based on hybrid recommendation which is the combination of content based and collaorative filtering and solves cold start problem .there are plans and services provided for a tourist plan for user

## screenshot of project
1.![msengage1](https://user-images.githubusercontent.com/91557659/170884951-0220e5d8-88f5-4f2b-978c-af26c9c9c15e.PNG)

2.![msengage2](https://user-images.githubusercontent.com/91557659/170885323-8e024351-09c1-4940-bb17-0be1c6a2a6ab.PNG)

3.![msengage3](https://user-images.githubusercontent.com/91557659/170885345-f92ce0fa-356f-4dc0-8f0d-938cd654ae0e.PNG)

4.![msengage4](https://user-images.githubusercontent.com/91557659/170885354-1412f9ae-7d71-472b-a121-8fd3f45d61c0.PNG)

5.![msengage5](https://user-images.githubusercontent.com/91557659/170885364-e44ada64-8fc7-42ee-b360-55f8fb640523.PNG)

6.![msengage6](https://user-images.githubusercontent.com/91557659/170885369-dc3c66bb-a007-4492-a592-2ff0196d09e5.PNG)
