import mysql.connector as connector
import config
import json
from mysql.connector import Error

configuration = config.mysql_credentials

# Loading the json file (car_parts_prices.json)
with open('car_parts_prices.json', 'r') as file:
    car_parts_prices = json.load(file)

try:
    connection = connector.connect(**configuration)
    if connection.is_connected():
        print("Connected to MySQL Database.")
        
        cursor = connection.cursor()

        # Loop through car_models dictionary and insert data into database
        for brand, models in car_parts_prices.items():
            for model, parts in models.items():
                for part, price in parts.items():
                    cursor.execute("INSERT INTO car_models (brand, model, part, price) VALUES (%s, %s, %s, %s)",
                                (brand, model, part, price))
                    
except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        # Commit changes and close connection
        cursor.close()
        connection.commit()
        connection.close()

        print("MySQL Connection is Closed.")

print("Data has been successfully inserted into the MySQL database.")