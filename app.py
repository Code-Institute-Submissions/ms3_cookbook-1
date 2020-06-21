import os
from flask import Flask, flash, render_template, redirect, request, url_for
import env as config
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

''' Database (mongoDB) confugirations: '''
app.config["MONGO_DBNAME"] = 'cook_book'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

''' Routes and viwes '''
@app.route('/')
# index - View of the landing page
@app.route('/index')
def index():

    recipe_numbers = mongo.db.recipes.count()
    return render_template('index.html', allrecipes=recipe_numbers)


# View from the newrecipe.html to add new recipes to the database
@app.route('/new_recipe')
def new_recipe():
    return render_template('newrecipe.html',
    categories=mongo.db.categories.find(),
    difficulty=mongo.db.difficulty.find())


# Insert_recipe function to add the recipe into the database
@app.route('/insert_recipe', methods=["GET", "POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    ingredients = request.form.get('ingredients').splitlines()
    instructions = request.form.get('recipe_instructions').splitlines()
    you_will_need = request.form.get('you_will_need').splitlines()

    if request.method == 'POST':
        add_recipe = {
            "recipe_name": request.form.get('recipe_name'),
            "recipe_info": request.form.get('recipe_info'),
            "cooking_time": request.form.get('cooking_time'),
            "category_name": request.form.get('category_name'),
            "servings_size": request.form.get('servings_size'),
            "recipe_difficulty": request.form.get('recipe_difficulty'),
            "ingredients": ingredients,
            "instructions": instructions,
            "you_will_need": you_will_need,
        }
    recipes.insert_one(add_recipe)
    flash('Recipe was added succesfully!')
    return redirect(url_for('index'))


# Show all existing recipes from the database
@app.route('/recipes')
def recipes():
    return render_template('recipes.html',
    recipes=mongo.db.recipes.find())


# Detailed page form the selected recipe
@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    _recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('showrecipe.html', recipe=_recipe)


# Contact us page
@app.route('/contact_us', methods=["GET", "POST"])
def contact_us():
    return render_template('contactus.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)