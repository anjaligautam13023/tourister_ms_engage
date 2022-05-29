from multiprocessing import context
from urllib import request

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from members.models import User
from members.tourist.algorithms.content_based import random_item
from members.tourist.algorithms.popular_places import popular_item
from members.tourist.algorithms.content_based import recommend
from members.tourist.algorithms.content_based import master_item
from members.tourist.algorithms.content_based import recomend_item
from members.tourist.algorithms.collaborative import collaborative_item
from members.models import Activity
from members.tourist.algorithms.hybrid import hybrid_recommendation
from members.tourist.algorithms.content_based import all_places


#function called at logout
def logout(request):
  #user name and id is set to null
  user= request.session['user_name'] = None
  request.session['user_id'] = None
  template = loader.get_template('html\logout.html')  
  return HttpResponse(template.render())


#function called at about 
def about(request):
  template = loader.get_template('html\\about.html')  
  user_name = request.session.get("user_name",None)
  #pssing user name to about page
  context = {
              'user_name': user_name
            }
  return HttpResponse(template.render(context,request))


#function called at index page
def index(request):
  template = loader.get_template('html/index.html')
  #get user name from session
  user_name = request.session.get("user_name",None)
  #get user id from session 
  id = request.session.get("user_id",None)   
  allPlaces=all_places()                       
  randomItem = random_item()

  #if user is not logged in then popularItem contains popular item else the item liked by similar users
  if user_name is None:
    popularItem=popular_item()
  else: 
    
    try:
      user=Activity.objects.get(id=id,name=user_name)
      popularItem=collaborative_item(id)
    except Activity.DoesNotExist:
      popularItem=popular_item()
    

  context = {'recommend': list,
              'random':randomItem,
              'popular':popularItem,
              'all_cities':allPlaces,
              'user_name': user_name
            }
  return HttpResponse(template.render(context,request))

#function called at when we click the image to view it
def page(request):
  if request.method == 'POST':
    place = request.POST.get("place")
    rating = request.POST.get("rating")
    #take user name from session
    user_name = request.session.get("user_name",None)
    #if user is logged in then save rating given by user to datbase
    #else add that place in database

    if user_name is  not None:
       #take user id from session
      id = request.session.get("user_id",None)
      try:
        user=Activity.objects.get(item=place,name=user_name)
        user.rate = rating
        user.save()
      except Activity.DoesNotExist:
        user = Activity(name = user_name,item=place,user_id=id,clicks=1,rate=rating)
        user.save()
      return JsonResponse({'success':'True'})
    else:
      return JsonResponse({'success':'False'})  

  else:
    place = request.GET.get("place")
    rc=recommend(place)
    all_cities=all_places()
    obj=master_item(rc)
    hybrid= hybrid_recommendation(place)
    user_name = request.session.get("user_name",None)
    #if user is logged in then save clicks by user to datbase
    #else add that place in database without rating
    if user_name is  not None:
      id = request.session.get("user_id",None)
      try:
        user=Activity.objects.get(item=place,name=user_name)
        user.clicks=user.clicks+1
        user.save()

      except Activity.DoesNotExist:
        user = Activity(name = user_name,item=place,user_id=id,clicks=1,rate=0)
        user.save()
    
    template = loader.get_template('html\page.html')
    recommend_image = recomend_item(rc)
    

    context = {
                  'recommend_image':recommend_image,
                  'mainobj': obj,
                  'user_name': user_name,
                  'all_cities':all_cities,
                  'hybrid':hybrid
                }
    return HttpResponse(template.render(context,request))  



    
#function to call at login 
@csrf_exempt
def login(request):
  template = None
  if request.method == 'POST':
    email=request.POST.get('email')
    password=request.POST.get('password')
    #taking user email and password from user and confirm it from database
    user = User(email = email,password=password)
    user= User.objects.get(email=email,password=password)
    #if user is not none then take user name and id
    if user is not None:
      request.session['user_name'] = user.name
      request.session['user_id'] = user.id
      return JsonResponse({'foo':'bar'})
    else:
      pass

  else:
    template = loader.get_template('html\login.html')
    return HttpResponse(template.render())  

#function to call at signup
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        #save user data to database
        user = User(name = name,email = email,password=password)
        user.save()
    template = loader.get_template('html\signup.html')
    return HttpResponse(template.render())