import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_sample_data(n_products=1000, n_users=500, n_ratings=5000):
    """Generate sample product, user, and rating data"""
    
    # Product categories and subcategories
    categories = {
        'Electronics': ['Smartphones', 'Laptops', 'Accessories', 'Audio', 'Gaming'],
        'Fashion': ['Men', 'Women', 'Kids', 'Footwear', 'Accessories'],
        'Home': ['Furniture', 'Decor', 'Kitchen', 'Bedding', 'Storage'],
        'Books': ['Fiction', 'Non-Fiction', 'Academic', 'Children', 'Comics'],
        'Sports': ['Equipment', 'Clothing', 'Shoes', 'Accessories', 'Nutrition']
    }
    
    # Product name templates
    product_templates = {
        'Electronics': ['{}Tech {}', '{}Smart {}', 'Pro {} {}', 'Ultra {} {}'],
        'Fashion': ['{} Style {}', '{} Fashion {}', 'Trendy {} {}', 'Classic {} {}'],
        'Home': ['{} Home {}', 'Modern {} {}', 'Luxury {} {}', 'Essential {} {}'],
        'Books': ['{} Guide to {}', 'The {} {}', 'Complete {} {}', 'Advanced {} {}'],
        'Sports': ['{} Sport {}', 'Professional {} {}', 'Elite {} {}', 'Premium {} {}']
    }
    
    # Generate products
    products = []
    product_id = 1001
    
    for category, subcategories in categories.items():
        n_category_products = n_products // len(categories)
        templates = product_templates[category]
        
        for _ in range(n_category_products):
            subcategory = random.choice(subcategories)
            price = round(random.uniform(10, 1000), 2)
            
            # Generate product name
            template = random.choice(templates)
            name = template.format(
                random.choice(['Premium', 'Deluxe', 'Basic', 'Pro', 'Ultra', 'Essential']),
                fake.word().title()
            )
            
            products.append({
                'product_id': product_id,
                'name': name,
                'category': category,
                'subcategory': subcategory,
                'price': price,
                'description': fake.text(max_nb_chars=200)
            })
            product_id += 1
    
    # Generate users
    users = []
    for user_id in range(1, n_users + 1):
        users.append({
            'user_id': user_id,
            'name': fake.name(),
            'email': fake.email(),
            'join_date': fake.date_between(start_date='-2y', end_date='today')
        })
    
    # Generate ratings
    ratings = []
    start_date = datetime.now() - timedelta(days=365)
    
    for _ in range(n_ratings):
        user_id = random.randint(1, n_users)
        product_id = random.randint(1001, 1001 + n_products - 1)
        rating = random.randint(1, 5)
        date = fake.date_time_between(start_date=start_date)
        
        ratings.append({
            'user_id': user_id,
            'product_id': product_id,
            'rating': rating,
            'timestamp': date,
            'review': fake.text(max_nb_chars=100) if random.random() > 0.3 else None
        })
    
    # Convert to DataFrames
    products_df = pd.DataFrame(products)
    users_df = pd.DataFrame(users)
    ratings_df = pd.DataFrame(ratings)
    
    # Create data directory
    import os
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    products_df.to_csv('data/products.csv', index=False)
    users_df.to_csv('data/users.csv', index=False)
    ratings_df.to_csv('data/ratings.csv', index=False)
    
    print(f"Generated and saved:")
    print(f"- {len(products_df)} products")
    print(f"- {len(users_df)} users")
    print(f"- {len(ratings_df)} ratings")

if __name__ == "__main__":
    generate_sample_data()
