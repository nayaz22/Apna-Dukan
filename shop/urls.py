
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='Shop Home'),
    path('about/',views.about,name='About'),
    path('contact/',views.contact,name='Contact'),
    path('tracker/',views.tracker,name='Tracker'),
    path('search/',views.search,name='Search'),
    path('product/<int:myid>',views.pv,name='Product View'),
    path('checkout/',views.checkout,name='Checkout'),
    path('handlerequest/',views.handlerequest,name='HandleRequest'),

]