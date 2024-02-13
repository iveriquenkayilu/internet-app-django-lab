# Import necessary classes
from django.http import HttpResponse
from .models import CarType, Vehicle, GroupMember, Buyer
from django.shortcuts import get_object_or_404
from django.views import View
from django.shortcuts import render


def practice(request, cartype_no):
    # get total price of all cars  of one type
    cartype = get_object_or_404(CarType, id=cartype_no)
    vehicles = Vehicle.objects.filter(car_type=cartype_no)
    # total_price = sum(vehicle.car_price for vehicle in vehicles)
    total_price = 0
    for vehicle in vehicles:
        total_price += vehicle.car_price
    interested_in = Buyer.objects.filter(interested_in=cartype_no).count()

    return HttpResponse(f"The total price is {total_price} " + f"{interested_in} people interested in it")


def homepage_old(request):
    cartype_list = CarType.objects.all().order_by('id')
    response = HttpResponse()
    heading1 = '<p>' + 'Different Types of Cars: ' + ' < / p > '
    response.write(heading1)
    for cartype in cartype_list:
        para = '<p>' + str(cartype.id) + ': ' + str(cartype) + '</p>'
        response.write(para)
    return response


# Yes, I am adding the the heading "Different Types of Cars"
def homepage(request):
    cartype_list = CarType.objects.all().order_by('id')
    context = {'cartype_list': cartype_list, 'heading1': 'Different Types of Cars'}
    return render(request, 'carapp/homepage.html', context)


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


def homepage2(request):
    cartype_list = Vehicle.objects.all().order_by('-car_price')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'Different Types of Cars: ' + ' < / p > '
    response.write(heading1)
    for cartype in cartype_list:
        para = '<p>' + str(cartype.id) + ': ' + str(cartype) + '</p>'
        response.write(para)
    return response

#No need to pass an extra context variable
def aboutus(request):
    return render(request, 'carapp/aboutus.html')

def aboutus2(request):
    response = HttpResponse()
    response.write("<h3>This is a Car Showroom </h3>")
    return response


def cardetail(request, cartype_no):
    car_type = get_object_or_404(CarType, pk=cartype_no)
    cars = Vehicle.objects.filter(car_type_id=cartype_no)
    heading1 = '<p>' + f'Vehicles of car type {cartype_no}: ' + ' </p> '
    response = HttpResponse()
    response.write(heading1)
    for cartype in cars:
        para = '<p>' + str(cartype.id) + ': ' + str(cartype) + '</p>'
        response.write(para)
    return response


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


class AboutUsView(View):

    def get(self, request):
        response = HttpResponse()
        response.write("<h3>This is a Car Showroom </h3>")
        return response

# Difference between FBV and CBV

# a) Class Based Views -> we need to import View from django.views and inherit View
# UNLIKE function based views
# b) Class based views -> we need to mention the request method
# UNLIKE function based views
# c)Class based views -> we need to use as_view() method in urls.py
# UNLIKE function based views
# Explanation : # URL dispatcher expects function as_view creates instance of class based view and determines
# appropriate HTTP handler in the view class if it exists else returns 405 method not allowed

# Pros Of Class Based Views
# class based views we do not have to use branching for different request methods like in function based views
# class based views improves reusability and seperation of concerns as they are
# Class based Views we can share variable among different request methods using class variables


# Class based view-
# 1.Object Oriented - acheives Abstraction ,Inheritance and Resuability
# Useful for Managing Complexity. Used in Larger Projects.
# 3.Provides predefined HTTP methods like get(),post().

# Function based view-
# 1.Not Object Oriented but are just functions
# 2.Used for simple prototypes or small projects.
# 3. HTTP methods should be handled using conditional statements.
