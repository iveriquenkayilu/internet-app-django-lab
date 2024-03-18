from django import forms
from django.contrib.auth.forms import UserCreationForm

from carapp.models import OrderVehicle, Vehicle, Buyer


class OrderVehicleForm(forms.ModelForm):
    class Meta:
        model = OrderVehicle
        fields = ['vehicle', 'buyer', 'quantity']  # vehicle_ordered
        widgets = {'buyer': forms.Select}
        labels = {'quantity': 'Vehicles Ordered'}  # Written this way to check it on the page


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    subject = forms.CharField(max_length=30)  # widget=forms.TextInput(attrs={''})
    message = forms.CharField(widget=forms.Textarea)


class VehicleSearchForm(forms.Form):
    id = forms.IntegerField()


class BuyerSignUpForm(UserCreationForm):
    # phone_number = forms.CharField(max_length=15)
    # address = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = ('username', 'email', 'phone_number', 'shipping_address')
