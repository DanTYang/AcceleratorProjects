from flask import Flask, request                                                                 
app = Flask(__name__)

restaurants = []
dishes = dict()
ratings = dict()

@app.route("/restaurants", methods=["POST", "GET"])
def restaurant_list():
    if request.method == 'GET':
        return "restaurants in the list: " + ", ".join(restaurants)
    else:
        restaurants.append(request.get_json()['restaurants'])
        dishes[request.get_json()['restaurants']] = []
        ratings[request.get_json()['restaurants']] = []
        return "Finished adding " + request.get_json()['restaurants'] + " to the list"
                                                 
@app.route("/restaurants/<name>", methods=["DELETE"])
def delete_restaurants(name):
    if(dishes.get(name, none):
        dishes[name] = []
    if(ratings.get(name, none):
        ratings[name] []
    restaurants.remove(name)
    del dishes[name]
    del ratings[name]
    return "Removed " + name + " from the list"
                                                                
@app.route("/restaurants/<name>/dishes", methods=["POST", "GET"])
def dishes_list(name):
    if request.method == "POST":
        list = dishes[name]
        list.append(request.get_json()['dishes'])
        dishes[name] = list
        return "Finished adding " + request.get_json()['dishes'] + " to " + name
    else:
        return "Dishes inside of " + name + ": " + ", ".join(dishes[name])

@app.route("/restaurants/<name>/ratings", methods=["POST", "GET"])
def ratings_list(name):
    if request.method == "POST":
        list = ratings[name]
        list.append(request.get_json()['ratings'])
        ratings[name] = list
        return "Finsihed adding " + request.get_json()['ratings'] + " to " + name
    else:
        return "Ratings inside of " + name + ": " + ", ".join(ratings[name])
