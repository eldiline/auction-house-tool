import requests
import json
import time

# BASIC FUNCTIONS
# ---------------------------------------------------

# Creates access token necessary for OAuth with givenid and password
def create_access_token(client_id, client_secret, region = 'eu'):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))
    return response.json()['access_token']

# Returns a list of connected realms
def connected_realms_list(token): 
    response = requests.get('https://eu.api.blizzard.com/data/wow/search/connected-realm?namespace=dynamic-eu&locale=en_GB&orderby=id&access_token='+token)
    results = response.json()['results']
    realms_nr = nr_conn_realms(token)
    data = list()   
    i = 0
    while i<realms_nr:
        data.append(results[i]['data'])
        i += 1
    return data

# Returns the number of connected realms
def nr_conn_realms(token):
    response = requests.get('https://eu.api.blizzard.com/data/wow/connected-realm/index?namespace=dynamic-eu&locale=en_GB&access_token='+token)
    return len(response.json()['connected_realms'])

# FUNCTIONS FOR DISPLAYING CHARACTER IMAGE
# -------------------------------------------

# Returns the image of a character
def get_character_img(charName, server, token):
    response = requests.get('https://eu.api.blizzard.com/profile/wow/character/'+server+'/'+charName.lower()+'/character-media?namespace=profile-eu&locale=en_GB&access_token='+token)
    img_link = ""

    try:
        if response.json().get('assets'):
            img_link = response.json()['assets'][2]['value']
        else:
            img_link = response.json()['render_url']
    except KeyError:
        img_link = ""
    return img_link

# Returns a list with all realm names
def get_realm_names(token):
    realm_list = connected_realms_list(token)
    realm_names = list()
    i=0
    while i<len(realm_list):
        realms = realm_list[i]['realms']
        j=0
        while j<len(realms):
            realm_names.append(realm_list[i]['realms'][j]['slug'])
            j += 1
        i+=1
    return realm_names

# FUNCTIONS FOR AUCTION HOUSE DISPLAY
# ---------------------------------------------------

# Returns all the auction listings for a connected realm
def get_auction_listing(realm_id, token):
    response = requests.get('https://eu.api.blizzard.com/data/wow/connected-realm/'+realm_id+'/auctions?namespace=dynamic-eu&locale=en_GB&access_token='+token)
    return response.json()

# Returns the cheapest listing for an item in a connected realm
def get_min_auction_listing(item_id, realm_id, token):
    with open(str(realm_id)) as f:
        json_file = json.load(f)
    auctions = json_file['auctions']
    i=0
    min_price = 10000000
    while i<len(auctions):
        curr_item_id = auctions[i]['item']['id']
        if curr_item_id == item_id:
            item_price = auctions[i]['unit_price']
            if item_price < min_price:
                min_price = item_price
        i+=1
    print(min_price)
    return min_price

# Returns a list of realms names included in the given connected realm ids
def get_realm_names_conn(conn_ids, token):
    realm_names = list()
    i=0
    while i<len(conn_ids):
        response = requests.get('https://eu.api.blizzard.com/data/wow/connected-realm/'+str(conn_ids[i])+'?namespace=dynamic-eu&access_token='+token)
        results = response.json()['realms']
        j=0
        while j<len(results):
           realm_names.append(results[j]['name']['en_US'])
           j+=1
        i+=1
    return realm_names

# Returns a dictionary containing the cheapest listing for an items along with the realms
def min_listing(item_id, token):
    start = time.time()
    i = 0
    id_list = get_conn_realm_id_list(token)
    min_price = 10000000
    chosen_realms = list()
    while i < len(id_list):
        curr_realm_price = get_min_auction_listing(item_id, id_list[i], token)
        if curr_realm_price < min_price:
            min_price = curr_realm_price
            chosen_realms.clear()
            chosen_realms.append(id_list[i])
        elif curr_realm_price == min_price:
            chosen_realms.append(id_list[i])
        i += 1
    realms = get_realm_names_conn(chosen_realms, token)
    results = {
        "realms": realms,
        "price": min_price
        }
    end = time.time()
    print(end - start)
    return results

# Returns a dictionary with all suggested items and their id based on user input
def get_item_list(item, token):
    response = requests.get('https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&locale=en_GB&name.en_GB='+item+'&orderby=id&_page=1&access_token='+token)
    results = response.json()['results']
    i = 0
    item_list = {}
    while i < response.json()['pageSize']:
        if item.lower() in results[i]['data']['name']['en_GB'].lower():
            item_list[results[i]['data']['name']['en_GB']] = results[i]['data']['id']
        i += 1
    return item_list

# Returns a list that contains the ids of all connected realms
def get_conn_realm_id_list(token):
    realm_list = connected_realms_list(token)
    id_list = list()
    i = 0
    while i<len(realm_list):
        id_list.append(realm_list[i]['id'])
        i += 1
    return id_list

# Returns the icon of an item
def get_item_icon(item_id, token):
    #response = requests.get('https://eu.api.blizzard.com/data/wow/media/item/'+str(item_id)+'?namespace=static-9.0.5_37760-eu&access_token='+token)
    print('response='+response)
    results = response.json()['assets'][0]['value']
    print(results)
    return results