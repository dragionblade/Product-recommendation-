import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_realistic_dataset():
    """Generate a realistic e-commerce dataset based on Amazon product patterns"""
    
    # Categories with subcategories
    categories = {
        'Electronics': ['Smartphones', 'Laptops', 'Cameras', 'Audio', 'Gaming'],
        'Fashion': ['Clothing', 'Shoes', 'Watches', 'Jewelry', 'Accessories'],
        'Home & Kitchen': ['Furniture', 'Appliances', 'Decor', 'Kitchen', 'Storage'],
        'Books': ['Fiction', 'Non-Fiction', 'Textbooks', 'Children', 'Comics'],
        'Beauty': ['Skincare', 'Makeup', 'Haircare', 'Fragrance', 'Tools'],
        'Sports': ['Exercise', 'Outdoor', 'Team Sports', 'Fitness', 'Accessories'],
        'Toys': ['Educational', 'Games', 'Outdoor', 'Arts & Crafts', 'Electronics'],
        'Automotive': ['Parts', 'Tools', 'Electronics', 'Interior', 'Exterior'],
        'Health': ['Vitamins', 'Medical Supplies', 'Personal Care', 'Wellness', 'Nutrition'],
        'Pet Supplies': ['Food', 'Toys', 'Health', 'Grooming', 'Accessories']
    }
    
    # Generate products (15,000 products)
    products = []
    product_id = 1
    
    for category, subcategories in categories.items():
        # Number of products per category (random between 1000-2000)
        n_products = np.random.randint(1000, 2000)
        
        for _ in range(n_products):
            subcategory = np.random.choice(subcategories)
            
            # Generate realistic price based on category
            if category in ['Electronics', 'Automotive']:
                price = np.random.lognormal(5, 1)  # Higher prices
            elif category in ['Books', 'Beauty', 'Pet Supplies']:
                price = np.random.lognormal(2.5, 0.5)  # Lower prices
            else:
                price = np.random.lognormal(4, 0.8)  # Medium prices
                
            # Generate realistic rating (slightly skewed towards positive)
            avg_rating = np.clip(np.random.normal(4.2, 0.5), 1, 5)
            rating_count = int(np.random.lognormal(5, 1))  # Some products very popular
            
            products.append({
                'product_id': product_id,
                'name': f"{category} Product {product_id}",
                'category': category,
                'subcategory': subcategory,
                'price': round(price, 2),
                'avg_rating': round(avg_rating, 1),
                'rating_count': rating_count,
                'description': f"This is a {subcategory} product in the {category} category."
            })
            product_id += 1
    
    # Convert to DataFrame
    products_df = pd.DataFrame(products)
    
    # Generate users (10,000 users)
    n_users = 10000
    users = []
    
    for user_id in range(1, n_users + 1):
        users.append({
            'user_id': user_id,
            'name': f"User_{user_id}",
            'email': f"user_{user_id}@example.com",
            'registration_date': datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
        })
    
    users_df = pd.DataFrame(users)
    
    # Generate ratings (100,000 ratings)
    n_ratings = 100000
    ratings = []
    
    # Users who rate more frequently
    active_users = np.random.choice(users_df['user_id'], size=int(n_users * 0.2))
    
    for _ in range(n_ratings):
        # 60% chance of rating coming from active users
        if np.random.random() < 0.6:
            user_id = np.random.choice(active_users)
        else:
            user_id = np.random.choice(users_df['user_id'])
            
        product = products_df.sample(n=1).iloc[0]
        
        # Rating tends to be close to product's average rating
        rating = np.clip(
            np.random.normal(product['avg_rating'], 0.5),
            1, 5
        )
        
        # Generate timestamp (more recent products have more recent ratings)
        days_ago = int(np.random.exponential(30))  # Exponential distribution for recency
        timestamp = datetime.now() - timedelta(days=days_ago)
        
        ratings.append({
            'user_id': user_id,
            'product_id': product['product_id'],
            'rating': round(rating, 1),
            'timestamp': timestamp
        })
    
    ratings_df = pd.DataFrame(ratings)
    
    # Save datasets
    print("Saving datasets...")
    products_df.to_csv('data/products.csv', index=False)
    users_df.to_csv('data/users.csv', index=False)
    ratings_df.to_csv('data/ratings.csv', index=False)
    
    print("\nDataset statistics:")
    print(f"Products: {len(products_df):,}")
    print(f"Users: {len(users_df):,}")
    print(f"Ratings: {len(ratings_df):,}")
    
    print("\nCategory distribution:")
    print(products_df['category'].value_counts())
    
    print("\nPrice statistics:")
    print(products_df['price'].describe())
    
    print("\nRating statistics:")
    print(ratings_df['rating'].describe())

if __name__ == "__main__":
    generate_realistic_dataset()
