from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def reg_validator(self, post):
        errors= {}
        if len(post['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters."
        if len(post['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters."
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post['email']) == 0: 
            errors['email'] = "Email is required."
        elif not email_regex.match(post['email']):
            errors['email'] = "Email is not valid."
        existing_email = User.objects.filter(email = post['email'])
        if len(existing_email) > 0:
            errors['registered'] = "This Email has already register."
        if len(post['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if post['password'] != post['password_confirm']:
            errors['confirmation'] = "Password not match."
        return errors
    
    def login_validator(self, post):
        errors = {}
        existing_user = User.objects.filter(email = post['email'])
        if len(existing_user) != 1:
            errors['email'] = "User does not exist."
        if len(post['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        elif bcrypt.checkpw(post['password'].encode(), existing_user[0].password.encode()) != True:
            errors['invalid'] = "Email and password do not match"
        return errors

    def password_change(self, post):
        errors = {}
        existing_user = User.objects.filter(id = post.session['user_id'])

        if bcrypt.checkpw(post['oldpassword'].encode(), existing_user[0].password.encode()) != True:
            errors['invalid'] = "Old password not correct."
        else:
            if len(post['password']) < 8:
                errors['password'] = "New password must be at least 8 characters."
            if post['password'] != post['password_confirm']:
                errors['confirmation'] = "Password not match."
        return errors

class MessageManager(models.Manager):
    def message_validator(self, post):
        errors={}
        if len(post['message']) == 0:
            errors['message'] = "Message can not be blank."
        return errors

class CommentManager(models.Model):
    def comment_validator(self, post):
        errors={}
        if len(post['comment']) == 0:
            errors['comment'] = "Comment can not be blank."
        return errors

class User (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    userlevel = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Message (models.Model):
    message_content = models.TextField()
    poster = models.ForeignKey(User, related_name= 'UserMessage', on_delete=models.CASCADE)
    created_for = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = MessageManager()

class Comment (models.Model):
    commnet_content = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='UserComment', on_delete=models.CASCADE)
    formessage = models.ForeignKey(Message, related_name='MessageComment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()