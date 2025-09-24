from django import forms
from .models import ShippingAddress 

class ShippingInfoForm(forms.ModelForm):
    shipping_full_name = forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"full name"}), required=True)
    shipping_email = forms.CharField(widget=forms.EmailInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"email"}), required=True)

    shipping_address1 = forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"shipping address"}), required=True)

    shipping_address2 = forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"shipping address"}), required=False)

    shipping_country= forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"shipping_country"}),required=True)

    shipping_state= forms.CharField(widget=forms.TextInput(attrs={"class":'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500','placeholder':"shipping state"}),required=False)

    shipping_city= forms.CharField(widget=forms.TextInput(attrs={"class":'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500','placeholder':"shipping city"}),required=True)

    shipping_postal_code= forms.CharField(widget=forms.TextInput(attrs={"class":'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500','placeholder':"shipping zip code"}),required=False)


    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['customer']
    
    def __str__(self):
        return f"{self.fullame} shipping information"


class PaymentForm(forms.Form):
    card_name= forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"full name on card"}), required=True)
    card_number= forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"card number"}), required=True)
    card_exp_date=forms.DateTimeField(widget=forms.DateInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"card expiry date"}), required=True)
    card_cvv_no=forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"card cvv code"}),required=True)
    card_country=forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"card country"}),required=True)
    card_city=forms.CharField(widget=forms.TextInput(attrs={"class":'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500','placeholder':"card city"}),required=True)
    card_address1=forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"card address 1"}), required=True)
    card_address2=forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"card address 2"}), required=False)
    card_zipcode=forms.CharField(widget=forms.TextInput(attrs={"class":'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500','placeholder':"card zip code"}),required=False)