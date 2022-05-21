from flask import jsonify, Blueprint, request, session

apiRickyAndMorty = Blueprint("apiRickyAndMort", __name__, url_prefix="/api/rickyAndMorty")

def getDataFromServer(url):
    import requests
    response = requests.get(url)

    return response.json()

responseFromApi = getDataFromServer('https://rickandmortyapi.com/api/character/')
results = responseFromApi['results']

@apiRickyAndMorty.route("/")
def gag():
    try:
        allElements = []
        for i in results:
            allElements.append({"name": i['name'], "gender": i['gender'], "image": i['image'], "episode": i['episode'][0]})
    
        return jsonify({"result": allElements})
    except Exception as e:
        return jsonify({"success": False, "message": "There is an error.."})


