from django import forms
from carapp.models import OrderVehicle


class OrderVehicleForm(forms.ModelForm):
    class Meta:
        model = OrderVehicle
        fields = ['vehicle', 'buyer', 'vehicles_ordered']
        widgets = {'buyer': forms.Select}
        labels = {'vehicle_ordered': 'Vehicle Ordered Label'}  # Written this way to check it on the page


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    subject = forms.CharField(max_length=30)  # widget=forms.TextInput(attrs={''})
    message = forms.CharField(widget=forms.Textarea)

