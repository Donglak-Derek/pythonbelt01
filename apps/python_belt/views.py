from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from django.core.urlresolvers import reverse

#landing page login and register
def index(response):
    return render(response, "python_belt/index.html")

#getting infos
def register(request):
    if User.userManager.isValidRegistration(request.POST, request):
        passFlag = True
        user1 = User.objects.get(email=request.POST['email'])
        request.session['user']=user1.id
        print request.POST , "ok"
        return redirect("/friends")
    else:
        passFlag = False
        print request.POST , "NO"
        return redirect("/main")

def login(request):
    if User.userManager.UserExistsLogin(request.POST, request):
        passFlag = True
        user1 = User.objects.get(email=request.POST['email'])
        request.session['user']=user1.id
        return redirect("/friends")  #redirect (reverse('friends'))
    else:
        passFlag = False
        return redirect ("/main")

# login and register sucess page
def friends(request):
    # if user1
    A = Follow.objects.get(id = 2)
    A.users.add(User.objects.get(id=1))
    print User.objects.all().values()
    
    context = {
        "all_friends": User.objects.all(),
        # "Ratings": Follow.objects.all(),
        # "Follows": Follow.objects.all()
        }
    # print Follow.objects.all()[0] , "in view"
    return render(request, "python_belt/friends.html", context)


#gettin friends infos
def profile(request):

    title = request.POST['User_title']
    
    if request.POST['new_author'] == '':
        author= request.POST['new_author']
    else:
        author=request.POST['author_list']
    User_one = User.objects.create(title = title, author= author) 
    # request.session['friends'] = User_one
    # # print User_one.objects.all() , "in view"
    Follow.objects.create(Follow = request.POST['Follow'], rating = int(request.POST['rating']), User_id=User_one.id, user_id=request.session['user'])
    return redirect('/friends/'+ str(User_one.id))

#display page
def display(request, id):
    A = User.objects.get(id = id)

    context ={
        "name": A.name,
        "alias": A.alias,
        "email": A.email,
        "bday": A.bday
    }
    print A.email
    return render(request, 'python_belt/User.html', context)

def logout(request):

    return redirect("/main")

def unfollow(request, id):
    # A = Follow.objects.delete(User.objects.get(id = id))
    # print A

    return redirect("/main")























