from flask import Flask, render_template
from flask import request, escape
import backend as f
import json


app = Flask(__name__)

# Creating OAuth token using credentials stored externally
with open("/home/ioana900/mysite/token_credentials.txt") as credentials_file:
    credentials = json.load(credentials_file)
client_id = credentials["client_id"]
client_secret = credentials["client_secret"]
token = f.create_access_token(client_id, client_secret)

realm_names = f.get_realm_names(token)

# Routes and renders the index page
@app.route('/')
def index():
    # Renders template along with realm names to create the realm list
    return render_template('index.html', realms=realm_names)

# Requests input submitted through form an creates list of suggested item
@app.route('/select-item', methods=["POST"])
def item_selection():
    if request.method == 'POST':
        charName = request.form['charName']
        realm = request.form['server']
        item = request.form['item']
        item_list = f.get_item_list(item, token)
        chosen_item = str(escape(request.args.get("chosen_item", "")))
    return render_template('item_selection.html', charName=charName, realm=realm, chosen_item=chosen_item, item_list=item_list)

# Requests input from item_selection, processes it and sends results to the html.
@app.route('/results', methods=["POST"])
def results():
    if request.method == 'POST':
        charName = request.form['charName']
        realm = request.form['realm']
        try:
            item = request.form['item']
            item_list = f.get_item_list(item, token)

            item_id = item_list.get(item)

            min_listing = f.min_listing(item_id, token)
            #item_img = f.get_item_icon(item_id, token)
            item_img = None
        except:
            print("There was an issue selecting the item.")
            min_listing = None
            item = None
            item_img = None
        try:
            img = f.get_character_img(charName, realm, token)
        except:
            print("There was an issue retrieving character media.")
            img = None
    return render_template('results.html', img=img, min_listing=min_listing, item=item, item_img=item_img)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)