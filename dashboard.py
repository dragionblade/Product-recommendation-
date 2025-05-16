import dash
from dash import html, dcc, Input, Output, State, no_update
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc

# Load data
products_df = pd.read_csv('data/products.csv')
ratings_df = pd.read_csv('data/ratings.csv')
users_df = pd.read_csv('data/users.csv')

# Calculate popularity score
products_df['popularity_score'] = products_df['avg_rating'] * np.log1p(products_df['rating_count'])

# Initialize the Dash app with a modern theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,  # Modern, flat design theme
        'https://use.fontawesome.com/releases/v5.15.4/css/all.css',
        'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css'
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Add loading component for better UX
app.config.suppress_callback_exceptions = True

# Create the layout
# Custom navbar with vibrant styling
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-analytics", 
                          style={"fontSize": "28px", "color": "#fff"}),
                    html.Span("E-Commerce Analytics", 
                             className="ms-3 h3",
                             style={"letterSpacing": "-0.5px", "fontWeight": "600"})
                ], style={
                    "display": "flex",
                    "alignItems": "center",
                    "background": "linear-gradient(90deg, #4361ee, #3a0ca3)",
                    "padding": "12px 25px",
                    "borderRadius": "12px",
                    "boxShadow": "0 4px 20px rgba(67, 97, 238, 0.3)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)"
                })
            ], width="auto"),
            dbc.Col([
                html.Div([
                    html.Button([
                        html.I(className="fas fa-filter me-2"),
                        "Filters"
                    ], id="filter-button", className="btn btn-light me-2"),
                    html.Div([
                        html.I(className="fas fa-clock me-2"),
                        html.Span("Updated: ", style={"fontWeight": "500"}),
                        html.Span(datetime.now().strftime("%B %d, %Y %H:%M"),
                                className="text-white-50")
                    ], className="d-flex align-items-center bg-dark px-3 py-1 rounded")
                ], className="d-flex align-items-center justify-content-end")
            ])
        ], align="center", className="g-0")
    ], fluid=True),
    color="dark",
    dark=True,
    className="mb-4 shadow-lg",
    style={
        "background": "rgba(15, 23, 42, 0.97)", 
        "backdropFilter": "blur(10px)",
        "borderBottom": "1px solid rgba(255, 255, 255, 0.1)"
    }
)

# Create callbacks for interactivity
@app.callback(
    Output("filter-modal", "is_open"),
    [Input("filter-button", "n_clicks"), Input("close-filter", "n_clicks")],
    [State("filter-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [Output("price-range-output", "children"),
     Output("filtered-products", "children")],
    [Input("price-range", "value"),
     Input("category-dropdown", "value")]
)
def update_filters(price_range, selected_categories):
    min_price, max_price = price_range
    
    # Filter by price
    filtered_df = products_df[(products_df['price'] >= min_price) & 
                             (products_df['price'] <= max_price)]
    
    # Filter by category if categories selected
    if selected_categories and len(selected_categories) > 0:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    
    return (
        f"Price Range: ${min_price} - ${max_price}",
        f"Showing {len(filtered_df)} products"
    )

# Layout
# Scroll to top button
scroll_to_top = html.Div(
    html.Button(
        html.I(className="fas fa-arrow-up"),
        id="scroll-to-top",
        className="scroll-to-top",
        n_clicks=0
    )
)

# Notification toast
notification = html.Div(
    id="notification-toast",
    className="notification-toast",
    children=[
        html.Div(id="notification-message", className="mb-0")
    ]
)

# Loading overlay
loading_overlay = dcc.Loading(
    id="loading-overlay",
    type="circle",
    fullscreen=True,
    className="loading-overlay"
)

# Add animation classes to cards
app.clientside_callback(
    """
    function(pathname) {
        // Add animation classes to cards with a staggered delay
        document.querySelectorAll('.card').forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('animate__animated', 'animate__fadeInUp');
        });
        
        // Add hover effects to charts
        document.querySelectorAll('.js-plotly-plot').forEach(chart => {
            chart.style.transition = 'all 0.3s ease';
            chart.style.borderRadius = '12px';
            
            chart.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.1)';
            });
            
            chart.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.05)';
            });
        });
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('url', 'pathname'),
    [Input('url', 'pathname')],
    prevent_initial_call=False
)

app.layout = dbc.Container([
    dcc.Store(id='filter-store', data={}),
    dcc.Location(id='url', refresh=False),
    loading_overlay,
    notification,
    scroll_to_top,
    navbar,
    
    # Filter Modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Dashboard Filters"), close_button=True),
            dbc.ModalBody([
                html.H6("Price Range", className="mt-3"),
                dcc.RangeSlider(
                    id="price-range",
                    min=int(products_df['price'].min()),
                    max=int(products_df['price'].max()),
                    step=5,
                    value=[int(products_df['price'].min()), int(products_df['price'].max() / 2)],
                    marks={i: f"${i}" for i in range(0, int(products_df['price'].max()) + 1, 100)},
                    className="mt-2 mb-4",
                ),
                html.Div(id="price-range-output", className="text-center mb-4"),
                
                html.H6("Categories", className="mt-3"),
                dcc.Dropdown(
                    id="category-dropdown",
                    options=[{"label": cat, "value": cat} for cat in sorted(products_df['category'].unique())],
                    multi=True,
                    placeholder="Select categories",
                    className="mb-4"
                ),
                
                html.Div(id="filtered-products", className="mt-3 text-center font-weight-bold")
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-filter", className="ms-auto")
            ),
        ],
        id="filter-modal",
        is_open=False,
        size="lg",
        backdrop="static",
    ),
    dbc.Row([
        dbc.Col([
            html.H1("Product Analysis Dashboard", className="text-primary text-center my-4"),
            html.Hr()
        ])
    ]),
    
    # Metric Cards with animations and accent colors
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-box fa-2x mb-3", style={"color": "#3498db"}),
                        html.H4(f"{len(products_df):,}", className="mb-1"),
                        html.P("Total Products", className="text-muted mb-0"),
                        html.Div([
                            html.Span(f"{len(products_df['category'].unique())} Categories", 
                                   className="badge bg-light text-primary mt-2")
                        ])
                    ], className="text-center")
                ])
            ], className="mb-4 metric-card hover-card card-accent-primary")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-users fa-2x mb-3", style={"color": "#2ecc71"}),
                        html.H4(f"{len(users_df):,}", className="mb-1"),
                        html.P("Total Users", className="text-muted mb-0"),
                        html.Div([
                            html.Span("Active Community", 
                                   className="badge bg-light text-success mt-2")
                        ])
                    ], className="text-center")
                ])
            ], className="mb-4 metric-card hover-card card-accent-success")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-star fa-2x mb-3", style={"color": "#f1c40f"}),
                        html.H4(f"{len(ratings_df):,}", className="mb-1"),
                        html.P("Total Ratings", className="text-muted mb-0"),
                        html.Div([
                            html.Span(f"Avg: {ratings_df['rating'].mean():.1f}/5", 
                                   className="badge bg-light text-warning mt-2")
                        ])
                    ], className="text-center")
                ])
            ], className="mb-4 metric-card hover-card card-accent-warning")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-dollar-sign fa-2x mb-3", style={"color": "#9b59b6"}),
                        html.H4(f"${products_df['price'].mean():.2f}", className="mb-1"),
                        html.P("Average Price", className="text-muted mb-0"),
                        html.Div([
                            html.Span(f"Range: ${products_df['price'].min():.0f}-${products_df['price'].max():.0f}", 
                                   className="badge bg-light text-info mt-2")
                        ])
                    ], className="text-center")
                ])
            ], className="mb-4 metric-card hover-card card-accent-info")
        ], width=3)
    ]),
    
    # Category Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5([
                        html.Span(className="me-2"),
                        html.I(className="fas fa-chart-bar me-2"),
                        "Category Analysis"
                    ], className="mb-0 d-flex align-items-center animate__animated animate__fadeInUp")
                ),
                dbc.CardBody([
                    dcc.Graph(
                        id='category-analysis-chart',
                        figure=px.bar(
                            products_df.groupby('category').agg({
                                'product_id': 'count',
                                'price': 'mean'
                            }).reset_index(),
                            x='category',
                            y=['product_id', 'price'],
                            barmode='group',
                            title='',
                            labels={'product_id': 'Number of Products', 'price': 'Average Price ($)', 'category': 'Category'},
                            color_discrete_sequence=['#4361ee', '#06d6a0']
                        ).update_layout(
                            plot_bgcolor='rgba(248, 249, 250, 0.5)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#2c3e50', 'family': 'Inter, sans-serif'},
                            showlegend=True,
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                            margin=dict(l=40, r=40, t=40, b=40),
                            xaxis=dict(
                                showgrid=False,
                                tickangle=45,
                                title=dict(font=dict(size=12))
                            ),
                            yaxis=dict(
                                showgrid=True,
                                gridcolor='rgba(236, 240, 241, 0.5)',
                                title=dict(font=dict(size=12))
                            ),
                            hoverlabel=dict(
                                bgcolor='white',
                                font_size=12,
                                font_family='Inter, sans-serif'
                            )
                        )
                    ),
                    html.Div([
                        html.Small(["Click on categories to filter - ", 
                                   html.A("Reset All", id="reset-filters", href="#", className="fw-bold text-primary")],
                                 className="text-muted mt-2")
                    ], className="text-center")
                ])
            ], className="mb-4 shadow-sm card-accent-primary hover-card animate__animated animate__fadeInUp")
        ])
    ]),
    
    # Price and Rating Distribution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5([
                        html.Span(className="me-2"),
                        html.I(className="fas fa-dollar-sign me-2"),
                        "Price Distribution"
                    ], className="mb-0 d-flex align-items-center animate__animated animate__fadeInUp")
                ),
                dbc.CardBody([
                    dcc.Graph(
                        id='price-distribution-chart',
                        figure=px.box(
                            products_df,
                            x='category',
                            y='price',
                            color='category',
                            title='',
                            labels={'price': 'Price ($)', 'category': 'Category'},
                            color_discrete_sequence=['#4361ee', '#06d6a0', '#ff9f1c', '#9b5de5', '#f15bb5', '#00bbf9', '#ff5a5f', '#0fa3b1', '#fb5607', '#7209b7']
                        ).update_layout(
                            plot_bgcolor='rgba(248, 249, 250, 0.5)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#2c3e50', 'family': 'Inter, sans-serif'},
                            showlegend=False,
                            margin=dict(l=40, r=40, t=40, b=80),
                            xaxis=dict(
                                showgrid=False, 
                                tickangle=45,
                                title=dict(font=dict(size=12))
                            ),
                            yaxis=dict(
                                showgrid=True, 
                                gridcolor='rgba(236, 240, 241, 0.5)',
                                title=dict(font=dict(size=12))
                            ),
                            hoverlabel=dict(
                                bgcolor='white',
                                font_size=12,
                                font_family='Inter, sans-serif'
                            )
                        ).update_traces(
                            boxmean=True,  # adds mean to box plots
                            line=dict(width=1.5),
                            marker=dict(size=3)
                        )
                    ),
                    html.Div([
                        html.Small(["Showing ", html.Strong("median"), " and ", html.Strong("quartile"), " ranges"], 
                                 className="text-muted mt-2")
                    ], className="text-center")
                ])
            ], className="mb-4 shadow-sm card-accent-info hover-card")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5([
                        html.Span(className="me-2"),
                        html.I(className="fas fa-star me-2"),
                        "Rating Distribution"
                    ], className="mb-0 d-flex align-items-center")
                ),
                dbc.CardBody([
                    dcc.Graph(
                        id='rating-distribution-chart',
                        figure=px.histogram(
                            ratings_df,
                            x='rating',
                            nbins=10,
                            title='',
                            labels={'rating': 'Rating', 'count': 'Number of Ratings'},
                            opacity=0.8,
                            color_discrete_sequence=['#ff9f1c']
                        ).update_layout(
                            plot_bgcolor='rgba(248, 249, 250, 0.5)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#2c3e50', 'family': 'Inter, sans-serif'},
                            showlegend=False,
                            bargap=0.1,
                            margin=dict(l=40, r=40, t=40, b=40),
                            xaxis=dict(
                                showgrid=False,
                                title=dict(font=dict(size=12)),
                                tickvals=[1, 2, 3, 4, 5]
                            ),
                            yaxis=dict(
                                showgrid=True, 
                                gridcolor='rgba(236, 240, 241, 0.5)',
                                title=dict(font=dict(size=12))
                            ),
                            hoverlabel=dict(
                                bgcolor='white',
                                font_size=12,
                                font_family='Inter, sans-serif'
                            )
                        ).add_annotation(
                            text=f'Average: {ratings_df["rating"].mean():.2f}/5',
                            xref='paper', yref='paper',
                            x=0.98, y=0.95,
                            showarrow=False,
                            font=dict(size=13, color='#2c3e50', family='Inter, sans-serif'),
                            bgcolor='rgba(255, 255, 255, 0.7)',
                            borderpad=4,
                            bordercolor='#f1c40f',
                            borderwidth=2
                        ).update_traces(
                            marker=dict(
                                line=dict(width=1, color='white'),
                                opacity=0.8
                            )
                        )
                    ),
                    html.Div([
                        html.Small(["Distribution across ", html.Strong(f"{len(ratings_df):,}"), " ratings"], 
                                 className="text-muted mt-2")
                    ], className="text-center")
                ])
            ], className="mb-4 shadow-sm card-accent-warning hover-card")
        ])
    ]),
    
    # Top Products
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5([html.I(className="fas fa-trophy me-2"), "Top Products"],
                            className="mb-0 d-flex align-items-center")
                ),
                dbc.CardBody([
                    dash.dash_table.DataTable(
                        data=products_df.nlargest(10, 'avg_rating')[
                            ['name', 'category', 'price', 'avg_rating', 'rating_count']
                        ].round(2).to_dict('records'),
                        columns=[
                            {'name': 'Name', 'id': 'name'},
                            {'name': 'Category', 'id': 'category'},
                            {'name': 'Price ($)', 'id': 'price'},
                            {'name': 'Avg Rating', 'id': 'avg_rating'},
                            {'name': 'Rating Count', 'id': 'rating_count'}
                        ],
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '15px',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'fontSize': '14px',
                            'fontFamily': '"Inter", -apple-system, sans-serif',
                            'color': '#2c3e50'
                        },
                        style_header={
                            'backgroundColor': '#ecf0f1',
                            'fontWeight': '600',
                            'textTransform': 'uppercase',
                            'fontSize': '12px',
                            'letterSpacing': '0.5px',
                            'color': '#2c3e50'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#f8f9fa'
                            }
                        ],
                        sort_action='native',
                        sort_mode='multi'
                    )
                ])
            ], className="mb-4 shadow-sm")
        ])
    ]),
    
    # Category Performance
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5([
                        html.Span(className="me-2"),
                        html.I(className="fas fa-chart-scatter me-2"),
                        "Category Performance"
                    ], className="mb-0 d-flex align-items-center")
                ),
                dbc.CardBody([
                    dcc.Graph(
                        id='category-performance-chart',
                        figure=px.scatter(
                            products_df,
                            x='price',
                            y='avg_rating',
                            color='category',
                            size='rating_count',
                            size_max=25,
                            hover_data=['name', 'rating_count', 'category'],
                            title='',
                            labels={
                                'price': 'Price ($)',
                                'avg_rating': 'Average Rating',
                                'rating_count': 'Number of Ratings',
                                'category': 'Category'
                            },
                            color_discrete_sequence=['#4361ee', '#06d6a0', '#ff9f1c', '#9b5de5', '#f15bb5', '#00bbf9', '#ff5a5f', '#0fa3b1', '#fb5607', '#7209b7']
                        ).update_layout(
                            plot_bgcolor='rgba(248, 249, 250, 0.5)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#2c3e50', 'family': 'Inter, sans-serif'},
                            showlegend=True,
                            legend=dict(
                                orientation='h',
                                yanchor='bottom',
                                y=1.02,
                                xanchor='right',
                                x=1,
                                title=None,
                                font=dict(size=10),
                                bgcolor='rgba(255, 255, 255, 0.8)',
                                bordercolor='rgba(0, 0, 0, 0.1)',
                                borderwidth=1
                            ),
                            margin=dict(l=40, r=40, t=40, b=40),
                            xaxis=dict(
                                showgrid=True,
                                gridcolor='rgba(236, 240, 241, 0.5)',
                                zeroline=False,
                                title=dict(font=dict(size=12))
                            ),
                            yaxis=dict(
                                showgrid=True,
                                gridcolor='rgba(236, 240, 241, 0.5)',
                                zeroline=False,
                                title=dict(font=dict(size=12)),
                                range=[0, 5.5]
                            ),
                            hoverlabel=dict(
                                bgcolor='white',
                                font_size=12,
                                font_family='Inter, sans-serif',
                                bordercolor='rgba(0,0,0,0.1)'
                            )
                        ).update_traces(
                            marker=dict(
                                line=dict(width=1, color='white'),
                                opacity=0.8
                            ),
                            hovertemplate="<b>%{customdata[0]}</b><br>" +
                                          "Category: %{customdata[2]}<br>" +
                                          "Price: $%{x:.2f}<br>" +
                                          "Rating: %{y:.1f}/5<br>" +
                                          "Reviews: %{customdata[1]}<extra></extra>"
                        )
                    ),
                    html.Div([
                        html.Small(["Bubble size represents number of ratings"], 
                                 className="text-muted mt-2")
                    ], className="text-center")
                ])
            ], className="mb-4 shadow-sm card-accent-success hover-card")
        ])
    ])
], fluid=True)

# Callback for scroll to top button
@app.callback(
    Output("scroll-to-top", "className"),
    [Input("url", "pathname")]
)
def toggle_scroll_button(pathname):
    return "scroll-to-top"

# Callback to show/hide scroll button based on scroll position
app.clientside_callback(
    """
    function(scroll_pos) {
        const show = scroll_pos > 300;
        return show ? 'scroll-to-top visible' : 'scroll-to-top';
    }
    """,
    Output("scroll-to-top", "className"),
    [Input("url", "pathname")],
    [State("url", "hash")]
)

# Callback for scroll to top functionality
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
        return window.scrollY;
    }
    """,
    Output("url", "hash"),
    [Input("scroll-to-top", "n_clicks")],
    prevent_initial_call=True
)

# Callback to show notification
@app.callback(
    [Output("notification-toast", "className"),
     Output("notification-message", "children")],
    [Input("filter-button", "n_clicks"),
     Input("apply-filters", "n_clicks")],
    [State("price-range-slider", "value"),
     State("category-dropdown", "value")]
)
def show_notification(filter_btn, apply_btn, price_range, categories):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "notification-toast", ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "apply-filters":
        message = "Filters applied successfully!"
        if price_range or categories:
            message += " "
            if price_range:
                message += f"Price: ${price_range[0]} - ${price_range[1]} "
            if categories:
                message += f"Categories: {', '.join(categories) if isinstance(categories, list) else categories}"
        return "notification-toast show", message
    
    return "notification-toast", ""

# Hide notification after delay
app.clientside_callback(
    """
    function(className) {
        if (className.includes('show')) {
            setTimeout(function() {
                var toast = document.querySelector('.notification-toast');
                if (toast) {
                    toast.className = 'notification-toast';
                }
            }, 5000);
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("notification-toast", "className"),
    [Input("notification-toast", "className")],
    prevent_initial_call=True
)

if __name__ == '__main__':
    app.run(debug=True, port=8053)
