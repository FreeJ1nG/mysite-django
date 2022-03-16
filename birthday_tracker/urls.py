from django.urls import path

from . import views

app_name = 'birthday_tracker'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:year>/<int:month>/', views.month_detail, name = 'month_detail'),
    path('<int:year>/<int:month>/<int:day>/', views.detail, name = 'detail'),
    path('insert_input/', views.insert_input, name = 'insert_input'),
    path('input/', views.input, name = 'input'),
]
