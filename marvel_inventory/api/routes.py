from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required, MarvelName
from marvel_inventory.models import db, MarvelHero, marvelhero_schema, marvelheroes_schema


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required 
def getdata(our_user):
    return{'some': 'value'}

#creat drone endpoint
@api.route('/heroes', methods = ['POST'])
@token_required
def create_hero(our_user):
    name = request.json['name']
    data = MarvelName(name)
    for i in data:
        marvel_id = i['id']
        name = i["name"]
        description = i["description"]
        img = i["thumbnail"]["path"] + '.' + i["thumbnail"]["extension"]
    user_token = our_user.token
    marvel_list = MarvelHero.query.filter_by(user_token = user_token)
    for i in marvel_list:
        if name == i.name:
            print("error")
            return jsonify()
    marvelhero = MarvelHero(marvel_id, name, description, img, user_token = user_token)
    db.session.add(marvelhero)
    db.session.commit()

    response = marvelhero_schema.dump(marvelhero)
    return jsonify(response)

@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_heroe(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        marvelhero = MarvelHero.query.get(id)
        response = marvelhero_schema.dump(marvelhero)
        return jsonify(response)
    else:
        return jsonify({'message' : 'balid id Required'}), 401
    
# RETRIEVE ALL DRONEs ENDPOINT
@api.route('/heroes', methods = ['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token
    marvelheroes = MarvelHero.query.filter_by(user_token = owner).all()
    response = marvelheroes_schema.dump(marvelheroes)
    return jsonify(response)



@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_heroes(our_user, id):
    marvelhero = MarvelHero.query.get(id)
    db.session.delete(marvelhero)
    db.session.commit()

    response = marvelhero_schema.dump(marvelhero)
    return jsonify(response)