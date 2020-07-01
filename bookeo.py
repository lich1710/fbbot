# Get game information from bookeo
# Insert information into a database

import os
import json
import requests
from bs4 import BeautifulSoup

import db

def fetch_games(API_SECRET_KEY, API_TOKEN_KEY, API_BASE_URL):
    # Call Bookeo API to get games information
    game_lists = get_games_info(API_SECRET_KEY, API_TOKEN_KEY, API_BASE_URL)

    if len(game_lists) > 0:
        # Get DB conn
        conn = db.get_conn()
        cursor = conn.cursor()

        # Insert into database
        for game in game_lists:
            cursor.execute('INSERT INTO games VALUES (?,?,?,?,?,?)', list(game.values()))

        # Commit
        conn.commit()

        # Print data inserted
        for row in cursor.execute('SELECT * FROM games'):
            print(row)
    else:
        print("Failed to fetch game from Bookeo.")

def get_games_info(API_SECRET_KEY, API_TOKEN_KEY, API_BASE_URL):
    headers = {
                'Content-Type': 'application/json',
                'X-Bookeo-secretKey': API_SECRET_KEY,
                'X-Bookeo-apiKey': API_TOKEN_KEY,
            }

    game_list = []

    # URL to get games info /settings/products
    # Language is Vietnamese
    api_url = '{0}settings/products'.format(API_BASE_URL)
    payload = { 'lang': 'vi-VN' }

    # Query and get response
    response = requests.get(api_url, headers=headers, params=payload)

    if response.status_code == 200:
        # Decode response payload into json
        json_response = json.loads(response.content.decode('utf-8'))

        game_id = 1
        # Extract game info from response data
        for game_info in json_response['data']:

            # Define a game structure
            tmp_game = {
                        "id": "",
                        "name": "",
                        "location": "",
                        "city": "",
                        "product_code": ""
                       }

            # Create temp object contain extracted data
            tmp_game['id'] = game_id
            tmp_game['name'] = game_info['name']
            tmp_game['product_code'] = game_info['productCode']

            # Extract city,location,weburl from description
            description = BeautifulSoup(game_info['description'], features="html.parser").text.split(';')
            # Verify description is in correct format
            if len(description) == 3:
                tmp_game['city'] = description[0]
                tmp_game['location'] = description[1]
                tmp_game['url'] = description[2]
            else:
                print(game_info['name'] + ' not containing correct description')
                continue

            # Only save games that allows API booking
            if game_info['apiBookingsAllowed']:
                game_list.append(tmp_game)
                game_id += 1

    else:
        print(response.content.decode('utf-8'))
    
    return game_list