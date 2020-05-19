from django.db import models
import re
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        logged_email = User.objects.filter(email=postData['email'])
        logged_username = User.objects.filter(username=postData['username'])

        if not email_check.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(logged_email) > 0:
            errors['email_in_use'] = "Email is already in use"
        if len(logged_username) > 0:
            errors['username_in_use'] = "Username is already in use"
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Password and Confirm password must match."
        if len(postData['username']) <4: 
            errors['username'] = "Username must be at least 4 characers."

        return errors

    def edit_validator(self, postData):
        errors = {}
        
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not email_check.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Password and Confirm password must match."

        return errors

class PostManager(models.Manager):
    def post_validator(self, postData):
        errors ={}
        if len(postData['post']) > 255:
            errors['post_too_long'] = "The post can only be 255 characters"
        if len(postData['post']) == 0:
            errors['post_empty'] = "Write a post"

        return errors

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors ={}
        if len(postData['comment']) > 255:
            errors['comment_too_long'] = "The comment can only be 255 characters"
        if len(postData['comment']) == 0:
            errors['comment_empty'] = "Write a comment"
        
        return errors

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    post = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='posts_posted', on_delete = models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    user_dislikes = models.ManyToManyField(User, related_name='disliked_posts')
    user_favorites = models.ManyToManyField(User, related_name='favorite_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete = models.CASCADE)
    post_comment = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()