from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from django.contrib import messages

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def isValidRegistration(self, userInfo, request):
        passFlag = True
        if not userInfo['name'].isalpha():
            messages.warning(request, 'No numbers for your NAME.')
            passFlag = False
        if len(userInfo['name']) < 2:
            messages.warning(request, 'more than 2 letters for your NAME.')
            passFlag = False
        if not userInfo['alias'].isalpha():
            messages.warning(request, 'Only alpha characters for your Alias!')
            passFlag = False
        if len(userInfo['alias']) < 2:
            messages.warning(request, 'more than 2 letters for your Alias!')
            passFlag = False
        if not EMAIL_REGEX.match(userInfo['email']):
            messages.warning(request, 'Email is not vaild!')
            passFlag = False
        if len(userInfo['password']) < 8:
            messages.warning(request, 'Password is too short.')
            passFlag = False
        if userInfo['password'] != userInfo['confirm_password']:
            messages.warning(request, "The passwords you've entered do not match.")
            passFlag = False
        # if not userInfo['bday'].isdigit():
        #     messages.warning(request, 'Only numbers for your bday!')
        #     passFlag = False
        # if len(userInfo['bday']) < 8:
        #     messages.warning(request, 'more than 2 letters for your bday!')
        #     passFlag = False
        if User.objects.filter(email = userInfo['email']):
            messages.error(request, "This email already exists in our database.")
            passFlag = False



        if passFlag == True:
            request.session['name'] = userInfo['name']
            print request.session['name'] ,"in models"
            messages.success(request, "Success! Welcome, " + request.session['name'] + "!")
            hashed = bcrypt.hashpw(userInfo['password'].encode(), bcrypt.gensalt())
            User.objects.create(name = userInfo['name'], alias = userInfo['alias'], email = userInfo['email'], password = hashed, bday= userInfo['bday'])
        return passFlag

    def UserExistsLogin(self, userInfo, request):
        passFlag = True
        if User.objects.filter(email = userInfo['email']):
            value = User.objects.filter(email = userInfo['email']).values()
            request.session['name'] = value[0]['name']
            hashed = User.objects.get(email = userInfo['email']).password
            hashed = hashed.encode('utf-8')
            password = userInfo['password']
            password = password.encode('utf-8')
            if bcrypt.hashpw(password, hashed) == hashed:
                # print userInfo['email'].all() ===>>>no all!!!!!
                messages.success(request, "Success! Welcome, " + request.session['name'] + "!")
                passFlag = True
            else:
                messages.warning(request, "Unsuccessful login. Incorrect password")
                passFlag = False
        else:
            request.session['name'] = ""
            messages.warning(request, "Your email is incorrect or not in our database.")
            passFlag = False
        return passFlag



class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    bday = models.DateTimeField()
    # followers = models.ManyToManyField(Follow, related_name = "users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    userManager = UserManager()
    objects = models.Manager()
    # def __repr__(self):
    #     return "<User object: {} {} {} {}>".format(self.name, self.alias, self.email, self.password)

 
class Follow(models.Model):
    follow = models.IntegerField()
    users = models.ManyToManyField(User, related_name = "followers")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # followers = models.ManyToManyField(Follow, related_name = "users")
    # def __repr__(self):
    #     return "<Book object: {} {}>".format(self.rating, self.review)
