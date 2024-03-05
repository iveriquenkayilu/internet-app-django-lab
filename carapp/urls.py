from django.urls import path
from . import views
from .views import AboutUsView, HomePage

app_name = 'carapp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    #path('', HomePage.as_view(), name='homepage'),
    #path('carapp/aboutus', views.aboutus, name='aboutus'),
    path('carapp/aboutus',views.aboutus , name='aboutus'), #AboutUsView.as_view()
    path('carapp/<int:cartype_no>', views.cardetail, name='cardetail'),
    #path('groupmembers/', views.groupmembers, name='groupmembers'),
    path('groupmembers/', views.GroupMemebers.as_view(), name='groupmembers'),

    path('carapp/vehicles', views.vehicles,name='vehicles'),
    path('carapp/order', views.orderhere, name='order')
]