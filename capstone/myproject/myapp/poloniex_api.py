import json
import plotly.graph_objects as go

# Read data from JSON file
with open(r'C:\Users\user\PycharmProjects\capstone\myproject\static\crypto_data.json', 'r') as file:
    data = json.load(file)

# Extract data for Bitcoin (BTC) and Ethereum (ETH)
btc_data = data['BTC']
eth_data = data['ETH']

# Function to create candlestick chart
def create_candlestick_chart(data, name, color):
    candlestick = go.Candlestick(x=[entry['Date'] for entry in data],
                                 open=[entry['Open'] for entry in data],
                                 high=[entry['High'] for entry in data],
                                 low=[entry['Low'] for entry in data],
                                 close=[entry['Close'] for entry in data],
                                 name=name,
                                 increasing_line_color=color,
                                 decreasing_line_color=color)
    return candlestick

# Create figure object
fig = go.Figure()

# Add Bitcoin (BTC) and Ethereum (ETH) candlestick charts to the figure
fig.add_trace(create_candlestick_chart(btc_data, name='Bitcoin (BTC)', color='green'))
fig.add_trace(create_candlestick_chart(eth_data, name='Ethereum (ETH)', color='red'))

# Customize layout
fig.update_layout(title='Candlestick Chart for Bitcoin (BTC) and Ethereum (ETH)',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  xaxis_rangeslider_visible=False,  # Disable range slider
                  template='plotly_dark',  # Dark theme
                  margin=dict(l=50, r=50, t=80, b=50),  # Adjust margins
                  font=dict(family='Arial', size=12, color='white'),  # Customize font
                  plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
                  hoverlabel=dict(bgcolor='black', font_size=12, font_family='Arial'),  # Customize hover label
                  showlegend=True  # Show legend
                  )

# Add gridlines and customize line width
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gray')

# Show figure
fig.show()