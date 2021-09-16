from django.urls import path

from store import views

app_name='store'

urlpatterns = [
    path('track/', views.track_product, name='track-product'),
]
