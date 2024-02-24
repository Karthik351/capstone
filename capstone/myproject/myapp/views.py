from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.shortcuts import render
import json
import plotly.graph_objects as go







@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('login')
    context = {'form': form}
    return render(request, 'myapp/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        '''customer.objects.create(
            user=user,
            name=user.username,
        )'''
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username Or Password is incorrect')

    context = {}
    return render(request, 'myapp/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def home(request):
    return render(request, 'myapp/home.html')






def candlestick_chart(request):
    with open(r'C:\Users\user\PycharmProjects\capstone\myproject\static\crypto_data.json', 'r') as file:
        data = json.load(file)

    btc_data = data['BTC']
    eth_data = data['ETH']

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

    fig = go.Figure()

    fig.add_trace(create_candlestick_chart(btc_data, name='Bitcoin (BTC)', color='green'))
    fig.add_trace(create_candlestick_chart(eth_data, name='Ethereum (ETH)', color='red'))

    fig.update_layout(title='Candlestick Chart for Bitcoin (BTC) and Ethereum (ETH)',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False,
                      template='plotly_dark',
                      margin=dict(l=50, r=50, t=80, b=50),
                      font=dict(family='Arial', size=12, color='white'),
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      hoverlabel=dict(bgcolor='black', font_size=12, font_family='Arial'),
                      showlegend=True)

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gray')

    chart_json = fig.to_json()

    return render(request, 'myapp/markets.html', {'btc_data': btc_data, 'eth_data': eth_data})








