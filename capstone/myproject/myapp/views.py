from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.shortcuts import render
import plotly.graph_objects as go
import requests
from .models import UserProfile, Investment, NewsArticle


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





def fetch_candlestick_data(symbol, interval, limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return data

def create_candlestick_chart(request):
    # Fetching data for BTC
    btc_data = fetch_candlestick_data("BTCUSDT", "1d")

    dates_btc = [item[0] for item in btc_data]
    opens_btc = [float(item[1]) for item in btc_data]
    highs_btc = [float(item[2]) for item in btc_data]
    lows_btc = [float(item[3]) for item in btc_data]
    closes_btc = [float(item[4]) for item in btc_data]

    candlestick_btc = go.Candlestick(x=dates_btc, open=opens_btc, high=highs_btc, low=lows_btc, close=closes_btc)

    # Fetching data for ETH
    eth_data = fetch_candlestick_data("ETHUSDT", "1d")

    dates_eth = [item[0] for item in eth_data]
    opens_eth = [float(item[1]) for item in eth_data]
    highs_eth = [float(item[2]) for item in eth_data]
    lows_eth = [float(item[3]) for item in eth_data]
    closes_eth = [float(item[4]) for item in eth_data]

    candlestick_eth = go.Candlestick(x=dates_eth, open=opens_eth, high=highs_eth, low=lows_eth, close=closes_eth)

    layout = go.Layout(title="Candlestick Chart", xaxis=dict(title="Date"), yaxis=dict(title="Price"))
    fig = go.Figure(data=[candlestick_btc, candlestick_eth], layout=layout)

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    return render(request, 'myapp/markets.html', {'plot_html': plot_html})





'''def portfolio(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    news = News.objects.all()[:5]  # Fetch latest 5 news
    context = {'user_profile': user_profile, 'news': news}
    return render(request, 'myapp/portfolio.html', context)'''



@login_required
def portfolio(request):
    user = request.user

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        btc_investment = Investment.objects.get(user=user, currency='BTC')
        eth_investment = Investment.objects.get(user=user, currency='ETH')
    except Investment.DoesNotExist:
        btc_investment = None
        eth_investment = None

    total_value = 0
    if btc_investment:
        total_value += btc_investment.amount * btc_investment.current_price
    if eth_investment:
        total_value += eth_investment.amount * eth_investment.current_price

    latest_news = NewsArticle.objects.order_by('-publish_date')[:5]

    context = {
        'user_profile': user_profile,
        'btc_investment': btc_investment,
        'eth_investment': eth_investment,
        'total_value': total_value,
        'latest_news': latest_news,
    }
    return render(request, 'myapp/portfolio.html', context)








