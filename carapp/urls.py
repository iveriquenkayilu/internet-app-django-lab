from django.urls import path, include
from . import views
from .views import BuyerSignUpView

app_name = 'carapp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    # path('', HomePage.as_view(), name='homepage'),
    # path('carapp/aboutus', views.aboutus, name='aboutus'),
    path('carapp/aboutus', views.aboutus, name='aboutus'),  # AboutUsView.as_view()
    path('carapp/<int:cartype_no>', views.cardetail, name='cardetail'),
    # path('groupmembers/', views.groupmembers, name='groupmembers'),
    path('groupmembers/', views.GroupMemebers.as_view(), name='groupmembers'),

    path('carapp/vehicles', views.vehicles, name='vehicles'),
    path('carapp/order', views.orderhere, name='order'),
    path('carapp/orderhere', views.orderhere, name='orderhere'),
    path('carapp/search', views.search, name='search'),

    path('signup/', BuyerSignUpView.as_view(), name='signup'), #SignUpView
    path('accounts/', include('django.contrib.auth.urls')),  # accounts pages

    path('login/', views.login_here, name='login'),
    path('logout/', views.logout_here, name='logout'),

    path('myorders', views.list_of_orders, name='list_of_orders')
]
