from django.shortcuts import render, redirect
from .models import User, Recipe, Comment
from django.contrib import messages
import bcrypt


# Create your views here.
def index (request):
    return render(request, "index.html")

def login_register (request):
    return render (request, "login_register.html")

def register (request):
    # Get Inputs and Validate
    errors = User.objects.validate_registration(request.POST)
    # If Validations do not pass
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/login_register")
    # If Validations Pass
    else:
        # Hash the passwords
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # Get inputs and create user
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_password
        )
    # Store new user id in session to use in redirect to personalized dashboard
    request.session['user_id'] = new_user.id
    return redirect("/dashboard")

def login (request):
    # Get inputs and validate
    errors = User.objects.validate_login(request.POST)
    # If Validations do not pass
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/login_register")
    else:
        user_list = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = user_list[0].id
        return redirect("/dashboard")

def dashboard (request):
    context ={
        "logged_in_user": User.objects.get(id=request.session['user_id']),
        "all_recipes":Recipe.objects.all()
    }
    return render (request, "dashboard.html", context)

def logout (request):
    # Clear session data to log out user return to index(login/register)
    request.session.clear()
    return redirect ("/")

def recipes (request):
    context ={
        "logged_in_user": User.objects.get(id=request.session['user_id']),
        "all_recipes": Recipe.objects.all()
    }
    return render (request, "recipes.html", context)

def create (request):
    context ={
        "logged_in_user": User.objects.get(id=request.session['user_id']),
    }
    return render (request, "create_recipe.html", context)

def process_create (request):
    # Get info and validate
    errors = Recipe.objects.validate_recipe(request.POST)
    # If validations do not pass
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/recipes/create")
    # If Validations pass
    else: 
        # Create instance of book object w/out many to mant attribute       
        user_from_db = User.objects.get(id = request.session["user_id"])
        new_recipe = Recipe.objects.create(
            title = request.POST["title"],
            ingredients = request.POST["ingredients"],
            description = request.POST["description"],
            instructions = request.POST["instructions"],
            notes = request.POST["notes"],
            creator = user_from_db,
        )
        #add many to many relationship
        new_recipe.favorited_by.add(user_from_db)
    return redirect (f"/recipes/{new_recipe.id}")

def view_recipe (request, recipe_id):
    recipe = Recipe.objects.get(id = recipe_id)
    ingredients = recipe.ingredients.split(",")
    instructions = recipe.instructions.split(",")
    notes = recipe.notes.split(",")
    context ={
        "logged_in_user": User.objects.get(id=request.session['user_id']),
        "this_recipe": recipe,
        "ingredients": ingredients,
        "instructions": instructions,
        "notes": notes,
        "comments": recipe.recipe_comments.order_by("-created_at")
    }
    return render (request, "view_recipe.html", context)

def edit(request, recipe_id):
    context = {
        "this_recipe": Recipe.objects.get(id=recipe_id)
    }
    return render (request, "edit.html", context)

def process_edit (request, recipe_id):
    # Get info and validate
    errors = Recipe.objects.validate_recipe(request.POST)
    # If validations do not pass
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/recipes/{recipe_id}/edit")
    # If Validations pass
    else: 
        update_recipe = Recipe.objects.get(id=recipe_id)
        update_recipe.title = request.POST["title"]
        update_recipe.ingredients = request.POST["ingredients"]
        update_recipe.description = request.POST["description"]
        update_recipe.instructions = request.POST["instructions"]
        update_recipe.notes = request.POST["notes"]
        update_recipe.save()
    return redirect (f"/recipes/{recipe_id}")

def delete (request, recipe_id):
    delete_recipe = Recipe.objects.get(id=recipe_id)
    delete_recipe.delete()
    return redirect("/dashboard")

def favorite (request, recipe_id):
    user_from_db = User.objects.get(id = request.session["user_id"]) 
    new_fav_recipe = Recipe.objects.get(id = recipe_id)
    new_fav_recipe.favorited_by.add(user_from_db)
    return redirect ("/dashboard")

def remove_favorite(request, recipe_id):
    user_from_db = User.objects.get(id = request.session["user_id"]) 
    remove_fav_recipe = Recipe.objects.get(id = recipe_id)
    remove_fav_recipe.favorited_by.remove(user_from_db)
    return redirect ("/dashboard")

def comment(request, recipe_id):
    errors = Comment.objects.validate_comment(request.POST)
    # If validations do not pass
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/recipes/{recipe_id}")
    # If Validations pass
    else: 
        # Create instance of comment object       
        user_from_db = User.objects.get(id = request.session["user_id"])
        new_comment = Comment.objects.create(
            user = user_from_db,
            recipe = Recipe.objects.get(id=recipe_id),
            content = request.POST["comment"],
        )
    return redirect (f"/recipes/{recipe_id}")

def delete_comment (request, recipe_id, comment_id):
    delete_comment = Comment.objects.get(id=comment_id)
    delete_comment.delete()
    return redirect(f"/recipes/{recipe_id}")