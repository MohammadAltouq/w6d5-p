from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from marvel_inventory.forms import HeroForm, searchName
from marvel_inventory.models import Hero, db, MarvelHero
from marvel_inventory.helpers import MarvelName

site = Blueprint('site', __name__ , template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods =['GET', 'POST'])
@login_required
def profile():
    my_hero = HeroForm()
    try:
        if request.method == 'POST' and my_hero.validate_on_submit():
            name = my_hero.name.data
            description = my_hero.description.data
            user_token = current_user.token

            hero = Hero(name, description, user_token)
            db.session.add(hero)
            db.session.commit()

            return redirect(url_for('site.profile'))
    
    except:
        raise Exception('Hero not created, please check your form and try again!')

    user_token = current_user.token

    hero = Hero.query.filter_by(user_token = user_token)
    marvel_list = MarvelHero.query.filter_by(user_token = user_token)


    return render_template('profile.html', form = my_hero, data = hero, mdata = marvel_list)
@site.route('/search', methods =['GET', 'POST'])
@login_required
def search():
    sw = searchName()
    user_token = current_user.token
    marvel_list = MarvelHero.query.filter_by(user_token = user_token)
    try:
        if request.method == 'POST' and sw.validate_on_submit():
            u_input = sw.name.data
            u_input = u_input.title()
            for i in marvel_list:
                if u_input == i.name:
                    print("error", i.name)
                    return redirect(url_for('site.search'))
            x = MarvelName(sw.name.data)
            for i in x:
                marvel_id = i['id']
                name = i["name"]
                description = i["description"]
                img = i["thumbnail"]["path"] + '.' + i["thumbnail"]["extension"]
                user_token = current_user.token

                marvelhero = MarvelHero(marvel_id, name, description, img, user_token)
                db.session.add(marvelhero)
                db.session.commit()
                return redirect(url_for('site.search'))
    except:
        raise Exception('Hero not created, please check your form and try again!')

    user_token = current_user.token

    marvel_list = MarvelHero.query.filter_by(user_token = user_token)

    return render_template('search.html',form = sw)

# hero_schema = HeroSchema()
# heroes_schema  = HeroSchema(many=True)
# marvelhero_schema = marvelSchema()
# marvelheroes_schema  = marvelSchema(many=True)