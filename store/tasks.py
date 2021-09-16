from django.core.mail import send_mail
from celery import shared_task
import schedule
import requests
from bs4 import BeautifulSoup
import time
from django.conf import settings

from store.models import Product

#@shared_task
def scrape_product(user, product_url, target_price):
    
    # Scrape info
    req = requests.get(product_url)
    soup = BeautifulSoup(req.text, 'lxml')
    
    #retrieve info
    title = soup.find('span', class_='B_NuCI').text
    product_price = soup.find('div', class_='_30jeq3').text[1:]
    product_image = soup.find('div', class_='q6DClP').attrs['style'][21:-6]

    if float(product_price) <= float(target_price):
        if not Product.objects.filter(user=user).filter(product_url=product_url).filter(completed=True).exists():

            print('sending mail')
            # send mail
            send_mail(
                f'Hey {user.username}! There\' s a price drop in a product. - Price Tracker',
                f'Whoa! A price just dropped for product {title}. Grab thea deal real quick.    Click on the link to view it.{product_url}.',
                settings.EMAIL_HOST_USER,
                [user.email, ],
                fail_silently=False,
            )
            product = Product.objects.get(product_url=product_url)
            product.completed = True
            product.save()
    
        

@shared_task
def monitor_price():
    products = Product.objects.all()
    for pro in products:
        job = schedule.every(10).seconds.do(scrape_product, user=pro.user, product_url=pro.product_url, target_price=pro.target_price)
        while True:
            schedule.run_pending()
            time.sleep(10)
            
            if pro.completed:
                schedule.cancel_job(job)



    #create product object
    #Product.objects.create(user=user, name=title, product_price=product_price, target_price=target_price, product_image=product_image)