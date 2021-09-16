from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import schedule

from store.models import Product
from store.tasks import monitor_price

# Create your views here.
def track_product(request):
    if request.method == 'POST':
        # Get form value
        product_url = request.POST['proUrl']
        target_price = int(request.POST['targetPrice'])


        # Scrape info
        #scrape_product(request.user, product_url, target_price)
        req = requests.get(product_url)
        soup = BeautifulSoup(req.text, 'lxml')
        
        #retrieve info
        title = soup.find('span', class_='B_NuCI').text
        product_price = soup.find('div', class_='_30jeq3').text[1:]
        product_image = soup.find('div', class_='q6DClP').attrs['style'][21:-6]
        
        #create product object
        Product.objects.create(user=request.user, name=title, product_price=product_price, target_price=target_price, product_image=product_image, product_url=product_url)

        # schedule
        monitor_price.delay()
        
        # redirect to dashboard
        return redirect('account:dashboard')
       

    return render(request, 'store/track.html', {})
