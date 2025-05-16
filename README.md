# E-Commerce Product Analysis Dashboard

A modern, interactive dashboard that analyzes product data and user ratings to generate insights and recommendations. The dashboard presents e-commerce analytics with a visually appealing interface and interactive features for data exploration.

## Overview

This project provides comprehensive analytics for product recommendation systems using a realistic dataset of over 12,500 products, 10,000 users, and 100,000 ratings. The dashboard offers interactive visualization and filtering capabilities to explore product performance across categories.

## Key Features

### 1. Interactive Data Visualization
- Dynamic charts and graphs with hover effects
- Interactive filters for data exploration
- Real-time data filtering by price range and category
- Responsive design for all screen sizes

### 2. Comprehensive Data Analysis
- Product performance metrics across categories
- User rating distribution and analysis
- Price analysis with statistical insights
- Top-performing products identification

### 3. Modern User Interface
- Vibrant color scheme with professional design
- Animated transitions and interactive elements
- Intuitive layout with clear data presentation
- Card-based design with accent colors for data categorization

### 4. Realistic Dataset
- 12,575 products across 10 diverse categories
- 10,000 user profiles with demographic information
- 100,000+ product ratings with timestamps
- Realistic price and rating distributions

## Project Structure

1. **Data Generation and Collection**
   - `generate_real_data.py`: Creates a realistic e-commerce dataset
   - `download_data.py`: Script for loading and processing data

2. **Dashboard and Visualization**
   - `dashboard.py`: Main dashboard application
   - `assets/styles.css`: Custom styling for the dashboard

3. **Data Analysis Components**
   - Category performance analysis
   - Price distribution visualization
   - Rating distribution analysis
   - Top products ranking

## 🚀 Installation and Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ecommerce-analytics-dashboard.git
   cd ecommerce-analytics-dashboard
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   # python -m venv venv
   # .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   python dashboard.py
   ```

5. **Access the dashboard**
   Open your browser and navigate to: http://127.0.0.1:8053/

## 📊 Features

- **Interactive Visualizations**: Explore data with interactive charts and graphs
- **Real-time Filtering**: Filter products by price range and category
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Dash**: Web application framework for building the dashboard
- **Plotly**: Interactive data visualization library
- **Pandas**: Data manipulation and analysis
- **Bootstrap**: Responsive design components

## 📂 Project Structure

```
ecommerce-analytics-dashboard/
├── dashboard.py          # Main dashboard application
├── assets/
│   └── styles.css       # Custom CSS styles
├── data/                 # Data files (not included in version control)
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```bash
# Clone the repository
git clone https://github.com/username/ecommerce-analytics-dashboard.git

# Navigate to project directory
cd ecommerce-analytics-dashboard

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python dashboard.py
```

## Technical Details

### Technologies Used
- **Dash & Plotly**: Interactive web-based visualizations
- **Pandas & NumPy**: Data manipulation and analysis
- **Bootstrap**: Responsive layout design
- **CSS3 Animations**: Enhanced user experience

### Data Processing Pipeline
1. Data generation with realistic distributions
2. Data cleaning and preprocessing
3. Feature engineering and statistical analysis
4. Interactive visualization

### Dashboard Components
- **Metric Cards**: Key performance indicators with animations
- **Category Analysis**: Interactive bar charts with filtering
- **Price Distribution**: Box plots with statistical indicators
- **Rating Analysis**: Histogram with detailed metrics
- **Performance Scatter Plot**: Multi-dimensional data visualization
- **Top Products Table**: Interactive sorting and filtering

## System Requirements
- Python 3.8+
- Modern web browser
- 4GB RAM (minimum)
- 100MB disk space

## Future Enhancements
- User behavior analytics integration
- Machine learning recommendations
- Time series analysis for seasonal trends
- Export functionality for reports

## License
MIT License

## Setup and Usage

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Generate sample data:
   ```bash
   python generate_sample_data.py
   ```

3. Run analysis:
   ```bash
   python product_analysis.py
   ```

## Output

The analysis generates:
1. `analysis_patterns.png`: Visualizations of key patterns
2. `analysis_summary.txt`: Detailed statistical summary
3. Console output with key findings

