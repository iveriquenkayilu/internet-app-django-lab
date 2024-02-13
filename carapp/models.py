from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CarType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.id) + " " + self.name


class Vehicle(models.Model):
    car_type = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
    car_name = models.CharField(max_length=200)
    car_price = models.DecimalField(max_digits=10, decimal_places=6)
    inventory = models.PositiveIntegerField(default=10)
    instock = models.BooleanField(default=True)
    # added
    description = models.TextField(blank=True, default='', max_length=150)

    def __str__(self):
        return str(self.id) + " " + self.car_name + " " + self.car_type.name + " " + str(self.car_price) + " " + str(
            self.inventory)


class Buyer(User):
    AREA_CHOICES = [('W', 'Windsor'), ('LS', 'LaSalle'), ('A', 'Amherstburg'), ('L', 'Lakeshore'), ('LE', 'Leamington'),
                    ('TO', 'Toronto'), ('CH', 'Chatham'), ('WA', 'Waterloo')]
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    area = models.CharField(max_length=2, choices=AREA_CHOICES, default='CH')
    interested_in = models.ManyToManyField(CarType)
    # added
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} stays at {self.shipping_address} {self.area}"


class OrderVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='orders', on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, related_name='orders', on_delete=models.CASCADE)
    # number of vehicles being ordered
    quantity = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = [
        (0, 'cancelled'),
        (1, 'placed'),
        (2, 'shipped'),
        (3, 'delivered'),
        (4, 'successful')
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle.car_name} ordered by {self.buyer.first_name} on {self.last_updated}"

    def total_price(self):
        return self.quantity * self.vehicle.car_price


class GroupMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    semester = models.IntegerField()
    link = models.URLField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} semester {self.semester}"

    class Meta:
        ordering = ['first_name']
