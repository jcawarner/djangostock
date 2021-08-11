from django.shortcuts import render,redirect
import requests
import json
from .models import Stock
from .form import StockForm
from django.contrib import messages


def home(request):
	#pk_f06822bd2bd44ab89170059647691815

	if request.method == 'POST':
		ticker = request.POST['ticker']

		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_f06822bd2bd44ab89170059647691815")
		
		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		return render(request, 'home.html', {'api': api})
	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above"})


def about(request):
	return render(request, 'about.html', {})

def add_stock(request):

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added"))
			return redirect('add_stock')

	else:
		ticker = Stock.objects.all()
		ouput = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_f06822bd2bd44ab89170059647691815")
		
			try:
				api = json.loads(api_request.content)
				ouput.append(api)
			except Exception as e:
				api = "Error..."
		return render(request, 'add_stock.html', {'ticker': ticker})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted!"))
	return redirect('add_stock')