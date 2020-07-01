import sqlite3
import db

# Get connection
conn = db.get_conn()
cursor = conn.cursor()

def get_cities():
    cities = [ row[0] for row in cursor.execute('SELECT distinct city FROM games;') ]
    
    return cities

def get_location_by_city(city):
    locations = [ row[0] for row in cursor.execute('SELECT distinct location FROM games where city=?;', (city,) ) ]

    return locations
        
def get_games_by_city(city):
    games = [ row[0] for row in cursor.execute('SELECT name FROM games where city=?;', (city,)) ]

    return games

def get_games_by_location(city, location):
    games = [ row[0] for row in cursor.execute('SELECT name FROM games where city=? and location=?;', (city, location,)) ]

    return games