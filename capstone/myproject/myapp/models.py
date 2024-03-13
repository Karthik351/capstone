# myapp/models.py
from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    btc_investment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    eth_investment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loss = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)



class Transaction(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  currency = models.CharField(max_length=10, choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum')])
  amount = models.DecimalField(max_digits=10, decimal_places=8)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  date = models.DateTimeField(auto_now_add=True)

  def get_profit_loss(self, current_prices):
    # Calculate profit or loss based on current price and purchase price
    current_value = self.amount * current_prices[self.currency]
    profit_loss = current_value - (self.amount * self.price)
    return profit_loss

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3)  # Assuming currency code like 'BTC' or 'ETH'
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    current_price = models.DecimalField(max_digits=20, decimal_places=2)

class NewsArticle(models.Model):
    title = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now_add=True)



