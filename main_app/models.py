from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        # Check Length of first_name: more than 1 Character
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Invalid First Name, must be longer than one Character"
        # Check Length of last_name: more than 1 Character
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Invalid Last Name, must be longer than one Character"
        # Check if first_name and last_name only contain alphabet characters
        if str.isalpha(postData['first_name']) == False or str.isalpha(postData['last_name']) == False:
            errors["first_name_alpha"] = "Invalid First Name or Last Name, can only contain alphabetic characters."

        # Check email follows email format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        # Check if email exists in DB
        user_list = User.objects.filter(email = postData['email'])
        if len(user_list) > 0:
            errors["email"] = "Invalid Credentials"
        # Assign input to variable
        user_list = User.objects.filter(email = postData['email'])
        if len(user_list) > 0:
            errors['duplicate_email'] = "Email not available, try again"
        # Check if password meets required minimum length
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        # Check if password matches confirm_password
        if postData['password'] != postData['confirm_password']:
            errors['password_match'] = "Passwords do not match"
        return errors

    def validate_login(self, postData):
        errors = {}
        # Check if email exists in DB
        user_list = User.objects.filter(email = postData['email'])
        if len(user_list) == 0:
            errors["email"] = "Invalid Credentials"
        else:
        # Validate Password
            logged_user = user_list[0]
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors['password'] = "Incorrect Credentials"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=55)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RecipeManager (models.Manager):
    def validate_recipe(self,postData):
        errors = {}
        # Validate Title Length
        if len(postData['title']) < 3:
            errors['title'] = "Invalid Title, must be longer than two Characters"
        # Validate Ingredients entry not empty
        if len(postData['ingredients']) < 3:
            errors['ingredients'] = "Invalid Ingredients, must be longer than two Characters"
        # Validate Description entry not empty
        if len(postData['description']) < 3:
            errors['description'] = "Invalid Description, must be longer than two Characters"
        # Validate Instuctions entry not empty
        if len(postData['instructions']) < 3:
            errors['instructions'] = "Invalid Instructions, must be longer than two Characters"
        return errors

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    instructions = models.TextField()
    notes = models.TextField(null = True)
    creator = models.ForeignKey(User, 
    related_name = "recipes", 
    on_delete = models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name = "fav_recipes")
    objects = RecipeManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentManager(models.Manager):
    def validate_comment(self, postData):
        errors = {}
        # Validate Comment Length
        if len(postData['comment']) < 3:
            errors['comment'] = "Invalid Comment, must be longer than two Characters"
        return errors

class Comment(models.Model):
    user = models.ForeignKey(User, related_name = "user_comments", on_delete = models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name = "recipe_comments", on_delete = models.CASCADE)
    content = models.TextField()
    objects = CommentManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)