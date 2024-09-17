from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    #  path('car/', views.car, name='car'),
    path('book/', views.book, name='book'),
    path('compare_cars/', views.compare_cars, name='compare_cars'),
    path('car/<int:car_id>/', views.car, name='car'),
    path('brand/',views.brand,name='brand'),
    path('brand/<str:make>/',views.car_list,name='car_list'),
    path('car_search/', views.car_search, name='car_search'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name = 'about'),
    path('add_funds/', views.add_funds, name='add_funds'),
    path('create-charge/', views.create_charge, name='create_charge'),
    path('Transaction/', views.Transaction, name='Transaction'),
    path('wallet/', views.wallet, name='wallet'),
    path('car_list/',views.car_list,name='car_list'),

]
