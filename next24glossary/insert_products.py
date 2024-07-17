from pymongo import MongoClient
from pymongo.server_api import ServerApi
# Connect to MongoDB
uri = "mongodb+srv://saiteja:saiteja@saidev.pmtwzvn.mongodb.net/?retryWrites=true&w=majority&appName=saidev"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client.groceryDB
products = db.products

# Sample products
sample_products = [
    {
        "name": "Apple",
        "price": 1.00,
        "description": "Fresh Red Apple",
        "image_url": "link_to_image"
    },
    {
        "name": "Banana",
        "price": 0.50,
        "description": "Fresh Yellow Banana",
        "image_url": "link_to_image"
    },
    {
        "name": "Carrot",
        "price": 0.30,
        "description": "Fresh Carrot",
        "image_url": "link_to_image"
    },
     {
        "name": "Mangoes",
        "price": 1.30,
        "description": "Fresh Mangoes",
        "image_url": "link_to_image"
    },
      {
        "name": "Soaps",
        "price": 3.30,
        "description": "fragnance soap",
        "image_url": "link_to_image"
    },
       {
        "name": "Buckets",
        "price": 5.30,
        "description": "Plastic bucket",
        "image_url": "link_to_image"
    },
        {
        "name": "Detergent",
        "price": 7.30,
        "description": "Blue Detergent",
        "image_url": "link_to_image"
    }
]

# Insert sample products
products.insert_many(sample_products)
print("Sample products inserted successfully!")
