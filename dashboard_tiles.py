# NOTE: this is a Proof of Concept script, please test before using in production!

# Copyright (c) 2021 Cisco and/or its affiliates.
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.0 (the "License"). You may obtain a copy of the
# License at
#                https://developer.cisco.com/docs/licenses
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

import requests
import json
from datetime import datetime
import os


def open_config():
    '''
    this function opens config.json
    '''
    if os.path.isfile("config.json"):
        global config_file
        with open("config.json", 'r') as config_file:
            config_file = json.loads(config_file.read())
            print("\nThe config.json file was loaded.\n")
    else:
        print("No config.json file, please make sure config.json file is in same directory.\n")



def write_config():
    ''' 
    This function writes to config.json
    '''
    with open("config.json", 'w') as output_file:
        json.dump(config_file, output_file, indent=4)

def get_CTR_access_token():
    ''' 
    This function requests access token for OAuth2 for other CTR API requests
    '''
    #error checking for API client details
    if config_file['client_id']:
        client_id = config_file['client_id']
    else:
        print("client_id is missing in config.json file...\n")

    if config_file['client_secret']:
        client_secret = config_file['client_secret']
    else:
        print("client_secret is missing in config.json file...\n")


    # create headers for access token request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }

    data = {
    'grant_type': 'client_credentials'
    }

    # create headers for access token request
    response = requests.post('https://visibility.amp.cisco.com/iroh/oauth2/token', headers=headers, data=data, auth=(client_id, client_secret))

    #check if request was succesful
    if response.status_code == 200:
        
        # grab the text from the request
        rsp_dict = json.loads(response.text)
        # retrieve variables from text, global variable so that it can be used by all functions for CTR
        access_token = (rsp_dict['access_token'])
        scope = (rsp_dict['scope'])
        expiration_time = (rsp_dict['expires_in'])     
        # user feedback
        #print(f"[200] Success, access_token generated! This is the scope: {scope}. Expires in: {expiration_time} seconds.\n") 
        
        # return token
        return access_token
    else:
        # user feedback
        print(f"Access token request failed, status code: {response.status_code}\n")

def return_all_available_tiles():
    '''
    this function returns all available tiles and modules for a SecureX org
    '''
    # create headers for API request
    bearer_token = 'Bearer ' + get_CTR_access_token()

    headers = {
        'Authorization': bearer_token,
        'Content-Type':'application/json',
        'Accept':'application/json'
        }
    
    # retrieve dispositions for observables
    response = requests.get('https://visibility.amp.cisco.com/iroh/iroh-dashboard/tiles', headers=headers)
    #print(response.text)
    return json.loads(response.text)

def return_data_from_tile(data_url,data_period):
    '''
    this function returns all data from a tile for a specific perdiod
    '''
    # create headers for API request
    bearer_token = 'Bearer ' + get_CTR_access_token()

    headers = {
        'Authorization': bearer_token,
        'Content-Type':'application/json',
        'Accept':'application/json'
        }

    concat_url = 'https://visibility.amp.cisco.com' + data_url
    params = {"period": data_period}
    
    # retrieve dispositions for observables
    response = requests.get(concat_url, headers=headers, params=params)
    #print(response.text)
    return json.loads(response.text)

### main script 
if __name__ == "__main__":
    # open config json file and grab client_id and secret
    open_config()
    
    returned_tiles = return_all_available_tiles()

    module_names = []

    # loop through all modules to get an overview
    for tile in returned_tiles['data']:
        if tile['module'] not in module_names:
            module_names.append(tile['module'])

    print(f"All available modules:\n\n{module_names}\n")

    off_switch_modules = True

    # small CLI hack to get tiles per module, and data from a tile
    while off_switch_modules:
        module_name = input("\nPlease copy paste the module name you wish to receive the tiles from [type 'exit' if done]: ")
        if module_name == "exit":
            off_switch_modules = False
            print("\nDone checking out modules for now!\n")
        else:
            print(f"Printing available tiles for {module_name}: \n")
            # loop through tiles of inputted module and print some infos
            for tile in returned_tiles['data']:
                if tile['module'] == module_name:
                    print(f"Tile title: {tile['title']}")
                    print(f"Tile data_url: {tile['data_url']}")
                    print(f"Tile available periods: {tile['periods']}\n")
            
            off_switch_tiles = True

            while  off_switch_tiles:
                data_url = input("Please copy paste the tile data_url you wish to receive the data from[type 'exit' if done]: ")
                
                if data_url == "exit":
                    off_switch_tiles = False
                    print("\nDone checking out tiles for now!\n")
                else:
                    data_period = input("Please copy paste the tile period you wish to receive the data from: ")
                    # call funtion that return data for tile
                    tile_data = return_data_from_tile(data_url,data_period)
                    print(f"\nData from tile below:\n\n{tile_data}\n")
            
            
        
