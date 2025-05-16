import pandas as pd
import numpy as np
from pathlib import Path
import requests
import os

def download_dataset():
    """
    Download Amazon Products dataset from Kaggle
    Dataset: https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset
    """
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Download URL (direct download link to avoid Kaggle API requirement)
    url = "https://raw.githubusercontent.com/piyushpatel2005/dataset-files/main/amazon_products.csv"
    
    print("Downloading dataset...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with open('data/amazon_products.csv', 'wb') as f:
            f.write(response.content)
        print("Download complete!")
    else:
        raise Exception("Failed to download dataset")

def process_dataset():
    """Process and clean the Amazon dataset"""
    print("Processing dataset...")
    
    # Read the dataset
    df = pd.read_csv('data/amazon_products.csv')
    
    # Clean and preprocess
    df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_count'] = df['rating_count'].str.replace(',', '').astype(float)
    
    # Extract main category
    df['main_category'] = df['category'].str.split('|').str[0]
    
    # Filter out products with no ratings or invalid prices
    df = df[
        (df['price'] > 0) & 
        (df['price'] < 10000) &  # Remove unrealistic prices
        (df['rating'].notna()) & 
        (df['rating_count'] > 10)  # Remove products with very few ratings
    ]
    
    # Select top categories by number of products
    top_categories = df['main_category'].value_counts().nlargest(10).index
    df = df[df['main_category'].isin(top_categories)]
    
    # Select relevant columns and rename
    products_df = df[[
        'product_id', 'product_name', 'main_category', 'price', 
        'rating', 'rating_count', 'description'
    ]].copy()
    
    products_df.columns = [
        'product_id', 'name', 'category', 'price',
        'avg_rating', 'rating_count', 'description'
    ]
    
    # Generate user data
    n_users = 10000
    users_df = pd.DataFrame({
        'user_id': range(1, n_users + 1),
        'name': [f"User_{i}" for i in range(1, n_users + 1)],
        'email': [f"user_{i}@example.com" for i in range(1, n_users + 1)]
    })
    
    # Generate ratings data
    n_ratings = 50000
    np.random.seed(42)
    
    ratings_df = pd.DataFrame({
        'user_id': np.random.choice(users_df['user_id'], n_ratings),
        'product_id': np.random.choice(products_df['product_id'], n_ratings),
        'rating': np.random.normal(
            products_df['avg_rating'].mean(), 
            0.5, 
            n_ratings
        ).clip(1, 5).round(1),
        'timestamp': pd.date_range(
            start='2023-01-01', 
            end='2024-12-31', 
            periods=n_ratings
        )
    })
    
    # Save processed datasets
    print("\nSaving processed datasets...")
    products_df.to_csv('data/products.csv', index=False)
    users_df.to_csv('data/users.csv', index=False)
    ratings_df.to_csv('data/ratings.csv', index=False)
    
    print(f"\nDataset statistics:")
    print(f"Products: {len(products_df):,}")
    print(f"Users: {len(users_df):,}")
    print(f"Ratings: {len(ratings_df):,}")
    
    # Print category distribution
    print("\nCategory distribution:")
    print(products_df['category'].value_counts())

if __name__ == "__main__":
    download_dataset()
    process_dataset()
