from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('sensors/', views.sensor),
    path('temperature/', views.temp, {'id': 1}, name='temperature'),
    path('temperature/<int:id>',views.temp),
    path('test/', views.test, {'id': 1},name='tabla'),
    path('test/<int:id>',views.test),
    path('humidity/', views.hum, {'id': 1}, name='humidity'),
    path('humidity/<int:id>',views.hum),
    path('air_quiality/', views.air, {'id': 1}, name='air_quality'),
    path('air_quiality/<int:id>',views.air),
    path('rtplot/', views.rtplot, name='rtplot'),

]
