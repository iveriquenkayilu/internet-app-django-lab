# Import necessary classes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect

from .forms import VehicleSearchForm, OrderVehicleForm, BuyerSignUpForm  # ContactUsForm
from .models import CarType, Vehicle, GroupMember, Buyer, OrderVehicle
from django.shortcuts import get_object_or_404
from django.views import View
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy


# Yes, I am adding the the heading "Different Types of Cars"
def homepage(request):
    visits = request.session.get('home_page_visit', 0)
    if visits is None:
        request.session['home_page_visit'] = 0
    else:
        visits += 1
        request.session['home_page_visit'] = visits

    cookie_value = request.COOKIES.get('home_page_visit', f'This is a default value')

    vehicles = Vehicle.objects.all().order_by('-car_price')
    context = {'vehicles': vehicles, 'heading1': 'Different Types of Cars', 'visits': visits,
               'cookie_value': cookie_value}
    response = render(request, 'carapp/homepage.html', context)
    response.set_cookie('home_page_visit', f'Old session value {visits}', max_age=3600, secure=True)
    return response

class HomePage(View):

    def get(self, request):
        cartype_list = Vehicle.objects.all().order_by('-car_price')[:10]
        response = HttpResponse()
        heading1 = '<p>' + 'Different Types of Cars: ' + ' < / p > '
        response.write(heading1)
        for cartype in cartype_list:
            para = '<p>' + str(cartype.id) + ': ' + str(cartype) + '</p>'
            response.write(para)
        return response


# No need to pass an extra context variable
def aboutus2(request):
    return render(request, 'carapp/aboutus.html')


def cardetail(request, cartype_no):
    car_type = get_object_or_404(CarType, pk=cartype_no)
    cars = Vehicle.objects.filter(car_type_id=cartype_no)
    context = {'cars': cars, 'cartype_no': cartype_no, 'cartype_name': car_type.name}
    return render(request, 'carapp/cardetail.html', context)


def vehicles(request):
    all_vehicles = Vehicle.objects.all()
    context = {'vehicles': all_vehicles}
    return render(request, 'carapp/vehicles.html', context)


def groupmembers(request):
    response = HttpResponse()
    members = GroupMember.objects.all().order_by('first_name')
    heading1 = '<p>' + f'Group members are : ' + ' </p> '
    response = HttpResponse()
    response.write(heading1)
    for member in members:
        para = '<p>' + f'{member.first_name} {member.last_name} semester: {member.semester} <a href="{member.link}"> Link </a>' + '</p>'
        response.write(para)
    return response


# class GroupMembers(View):
# do it in 3 ways, using the Model and not using the model

# 1)
class GroupMemebers(View):
    # model = GroupMember
    # template_name = 'carapp\\groupmembers.html'
    # context_object_name = 'groupmembers'

    def get(self, request):
        members = GroupMember.objects.all().order_by('first_name')
        return render(request, 'carapp/groupmembers.html', {'members': members})


class AboutUsView(View):

    def get(self, request):
        response = HttpResponse()
        response.write("<h3>This is a Car Showroom </h3>")
        return response


def aboutus(request):
    form = VehicleSearchForm(request.GET)
    vehicles = Vehicle.objects.all()

    if form.is_bound and form.is_valid:  # Checking if form is valid
        if 'id' in form.data:
            id = form.data['id']
            vehicle = get_object_or_404(Vehicle, pk=id)  # Retrieving vehicle by primary key
            orders = Vehicle.objects.filter(car_price__lt=30000)
            return render(request, "carapp/aboutus.html", {'found': vehicle, 'vehicles': vehicles, 'orders': orders})

    return render(request, "carapp/aboutus.html", {'vehicles': vehicles})


# def contactusview(request):
# data = {'name': 'Iverique'}
# form = ContactUsForm(data) #Can be empty inially
# form = ContactUsForm(request.POST)  #to bind data, populate it with submitted data
# return "render(request, template, context)"


def search(request):
    form = VehicleSearchForm(request.GET)
    vehicles = Vehicle.objects.all()

    if form.is_bound and form.is_valid:  # Checking if form is valid
        if 'id' in form.data:
            id = form.data['id']
            vehicle = get_object_or_404(Vehicle, pk=id)  # Retrieving vehicle by primary key
            return render(request, "carapp/search_vehicle.html", {'found': vehicle, 'vehicles': vehicles})

    return render(request, "carapp/search_vehicle.html", {'vehicles': vehicles})


def orderhere(request):
    msg = ''
    vehiclelist = Vehicle.objects.all()
    if request.method == 'POST':
        form = OrderVehicleForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # if order.vehicle.orders <= order.vehicle.instock:
            # if order.vehicle.orders.count() <= order.vehicle.inventory:
            if order.quantity <= order.vehicle.inventory:
                order.vehicle.inventory -= order.quantity  # order.quantity
                order.vehicle.save()
                order.save()
                msg = 'Your vehicle has been ordered'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'carapp/nosuccess_order.html', {'msg': msg})
    else:
        form = OrderVehicleForm()
    return render(request, 'carapp/orderhere.html', {'form': form, 'msg': msg, 'vehiclelist': vehiclelist})


class SignUpView(CreateView):
    form_class = UserCreationForm
    # this is not working well
    success_url = reverse_lazy("carapp:login")  # for class based, instead of  reverse('carapp:login')
    template_name = 'carapp/signup.html'


class BuyerSignUpView(CreateView):
    form_class = BuyerSignUpForm
    success_url = reverse_lazy('carapp:login')
    template_name = 'carapp/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_buyer = True
        user.save()
        return super().form_valid(form)


# Create your views here.
def login_here(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('carapp:homepage'))
            else:
                return HttpResponse('Your account is disabled')
        else:
            return HttpResponse('Login details are incorrect')
    else:
        return render(request, 'carapp/login_here.html')


@login_required
def logout_here(request):
    logout(request)
    # return HttpResponseRedirect(reverse('carapp:homepage'))
    return HttpResponseRedirect('/')


@login_required
def list_of_orders(request):
    print("User getting all orders")

    is_user_buyer = hasattr(request.user, 'buyer')
    if is_user_buyer:
        orders = OrderVehicle.objects.filter(buyer=request.user.buyer)
        context = {'orders': orders, 'is_user_buyer': is_user_buyer}
        return render(request, 'carapp/list_of_orders.html', context)
    else:
        return render(request, 'carapp/list_of_orders.html', {'orders': [], 'is_user_buyer': False})
