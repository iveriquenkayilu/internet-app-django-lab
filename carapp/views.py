# Import necessary classes
from django.http import HttpResponse

from .forms import VehicleSearchForm, OrderVehicleForm  # ContactUsForm
from .models import CarType, Vehicle, GroupMember, Buyer
from django.shortcuts import get_object_or_404
from django.views import View
from django.shortcuts import render


# Yes, I am adding the the heading "Different Types of Cars"
def homepage(request):
    vehicles = Vehicle.objects.all().order_by('-car_price')
    context = {'vehicles': vehicles, 'heading1': 'Different Types of Cars'}
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


# No need to pass an extra context variable
def aboutus(request):
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
            if order.vehicle.orders.count() <= order.vehicle.inventory:
                order.vehicle.inventory -= 1
                order.vehicle.save()
                order.save()
                msg = 'Your vehicle has been ordered'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'carapp/nosuccess_order.html', {'msg': msg})
    else:
        form = OrderVehicleForm()
    return render(request, 'carapp/orderhere.html', {'form': form, 'msg': msg, 'vehiclelist': vehiclelist})
