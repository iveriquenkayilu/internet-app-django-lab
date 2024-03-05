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


# No need to pass an extra context variable
def aboutus(request):
    return render(request, 'carapp/aboutus.html')


def aboutus2(request):
    response = HttpResponse()
    response.write("<h3>This is a Car Showroom </h3>")
    return response


def cardetail(request, cartype_no):
    car_type = get_object_or_404(CarType, pk=cartype_no)
    cars = Vehicle.objects.filter(car_type_id=cartype_no)
    context = {'cars': cars, 'cartype_no': cartype_no, 'cartype_name': car_type.name}
    return render(request, 'carapp/cardetail.html', context)


def vehicles(request):
    all_vehicles = Vehicle.objects.all()
    context = {'vehicles': all_vehicles}
    return render(request, 'carapp/vehicles.html', context)


def orderhere(request):
    return render(request, 'carapp/orderhere.html')


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
