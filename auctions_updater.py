import backend as be
import time
import os
import json

# Creating OAuth token using credentials stored externally
with open("token_credentials.txt") as credentials_file:
    credentials = json.load(credentials_file)
client_id = credentials["client_id"]
client_secret = credentials["client_secret"]
# token = f.create_access_token(client_id, client_secret)

token = be.create_access_token(client_id, client_secret)
id_list = be.get_conn_realm_id_list(token)

i = 0
while i < len(id_list):
    id_string = str(id_list[i])
    f = open(id_string, "w")
    try:
        f.write(str(be.get_auction_listing(id_string, token)).replace("\'", "\""))
        i+=1
    except:
        print("Disconnected from server. Trying again..")
    f.close()
    print(id_string)