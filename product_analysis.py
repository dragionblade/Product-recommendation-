import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class ProductAnalysis:
    def __init__(self):
        self.products_df = None
        self.ratings_df = None
        self.users_df = None
        self.cleaned_data = None
        
    def load_data(self, products_path, ratings_path, users_path):
        """
        Load data from multiple sources and perform initial checks
        """
        print("1. Data Loading and Initial Checks")
        print("---------------------------------")
        
        # Load datasets
        self.products_df = pd.read_csv(products_path)
        self.ratings_df = pd.read_csv(ratings_path)
        self.users_df = pd.read_csv(users_path)
        
        # Display initial information
        print("\nProducts Dataset:")
        print(f"Shape: {self.products_df.shape}")
        print("\nMissing Values:")
        print(self.products_df.isnull().sum())
        
        print("\nRatings Dataset:")
        print(f"Shape: {self.ratings_df.shape}")
        print("\nMissing Values:")
        print(self.ratings_df.isnull().sum())
        
        return self.products_df, self.ratings_df, self.users_df
    
    def clean_data(self):
        """
        Clean data by handling missing values, duplicates, and inconsistencies
        """
        print("\n2. Data Cleaning")
        print("---------------")
        
        # Handle missing values
        imputer = SimpleImputer(strategy='mean')
        numeric_columns = self.products_df.select_dtypes(include=[np.number]).columns
        self.products_df[numeric_columns] = imputer.fit_transform(self.products_df[numeric_columns])
        
        # Remove duplicates
        initial_products = len(self.products_df)
        initial_ratings = len(self.ratings_df)
        
        self.products_df.drop_duplicates(inplace=True)
        self.ratings_df.drop_duplicates(inplace=True)
        
        print(f"\nDuplicates removed from products: {initial_products - len(self.products_df)}")
        print(f"Duplicates removed from ratings: {initial_ratings - len(self.ratings_df)}")
        
        # Handle inconsistent categories
        self.products_df['category'] = self.products_df['category'].str.strip().str.title()
        
        return self.products_df, self.ratings_df
    
    def feature_engineering(self):
        """
        Create new features and select relevant ones for analysis
        """
        print("\n3. Feature Engineering")
        print("--------------------")
        
        # Create new features
        self.products_df['price_category'] = pd.qcut(self.products_df['price'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        
        # Calculate product metrics
        product_metrics = self.ratings_df.groupby('product_id').agg({
            'rating': ['count', 'mean', 'std']
        }).reset_index()
        product_metrics.columns = ['product_id', 'rating_count', 'avg_rating', 'rating_std']
        
        # Merge with products
        self.products_df = self.products_df.merge(product_metrics, on='product_id', how='left')
        
        # Create popularity score
        self.products_df['popularity_score'] = self.products_df['avg_rating'] * np.log1p(self.products_df['rating_count'])
        
        print("\nNew Features Created:")
        print("- price_category: Price range categorization")
        print("- rating_count: Number of ratings per product")
        print("- avg_rating: Average rating per product")
        print("- rating_std: Rating standard deviation")
        print("- popularity_score: Combined score of rating and count")
        
        return self.products_df
    
    def analyze_patterns(self):
        """
        Identify patterns, trends, and anomalies in the data
        """
        print("\n4. Pattern Analysis")
        print("-----------------")
        
        # Analyze rating distribution
        plt.figure(figsize=(15, 5))
        
        plt.subplot(1, 3, 1)
        sns.histplot(self.ratings_df['rating'], bins=10)
        plt.title('Rating Distribution')
        
        plt.subplot(1, 3, 2)
        sns.boxplot(data=self.products_df, y='price', x='category')
        plt.xticks(rotation=45)
        plt.title('Price Distribution by Category')
        
        plt.subplot(1, 3, 3)
        sns.scatterplot(data=self.products_df, x='price', y='avg_rating', 
                       size='rating_count', hue='category', alpha=0.6)
        plt.title('Price vs Rating by Category')
        plt.tight_layout()
        plt.savefig('analysis_patterns.png')
        
        # Identify outliers
        print("\nOutlier Analysis:")
        numeric_cols = ['price', 'avg_rating', 'rating_count']
        for col in numeric_cols:
            Q1 = self.products_df[col].quantile(0.25)
            Q3 = self.products_df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = len(self.products_df[(self.products_df[col] < (Q1 - 1.5 * IQR)) | 
                                         (self.products_df[col] > (Q3 + 1.5 * IQR))])
            print(f"- {col}: {outliers} outliers detected")
    
    def generate_summary(self):
        """
        Generate summary statistics and key insights
        """
        print("\n5. Summary Statistics and Insights")
        print("--------------------------------")
        
        # Category analysis
        category_stats = self.products_df.groupby('category').agg({
            'product_id': 'count',
            'price': ['mean', 'std'],
            'avg_rating': 'mean',
            'rating_count': 'sum'
        }).round(2)
        
        print("\nCategory Analysis:")
        print(category_stats)
        
        # Top performing products
        print("\nTop 5 Products by Popularity:")
        top_products = self.products_df.nlargest(5, 'popularity_score')[
            ['name', 'category', 'price', 'avg_rating', 'rating_count']
        ]
        print(top_products)
        
        # Price-rating correlation
        correlation = self.products_df['price'].corr(self.products_df['avg_rating'])
        print(f"\nPrice-Rating Correlation: {correlation:.2f}")
        
        # Save summary to file
        with open('analysis_summary.txt', 'w') as f:
            f.write("Product Analysis Summary\n")
            f.write("======================\n\n")
            f.write(f"Total Products: {len(self.products_df)}\n")
            f.write(f"Total Ratings: {len(self.ratings_df)}\n")
            f.write(f"Average Rating: {self.ratings_df['rating'].mean():.2f}\n")
            f.write(f"Price-Rating Correlation: {correlation:.2f}\n")
            
    def run_full_analysis(self, products_path, ratings_path, users_path):
        """
        Run the complete analysis pipeline
        """
        self.load_data(products_path, ratings_path, users_path)
        self.clean_data()
        self.feature_engineering()
        self.analyze_patterns()
        self.generate_summary()
        
if __name__ == "__main__":
    analyzer = ProductAnalysis()
    analyzer.run_full_analysis('data/products.csv', 'data/ratings.csv', 'data/users.csv')
