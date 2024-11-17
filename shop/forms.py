from django import forms
from .models import ProductEntry, Product, Category, Order
from django import forms
from .models import Order

from cities_light.models import Country, Region



class ProductEntryForm(forms.ModelForm):
    class Meta:
        model = ProductEntry
        fields = ['product', 'quantity', 'selling_price']


from django import forms
from cities_light.models import Country
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'country', 'category', 'image', 'variations'] 

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from kwargs
        super(ProductForm, self).__init__(*args, **kwargs)

        # Populate the country field with all countries from cities-light
        self.fields['country'].queryset = Country.objects.all()  # Get all countries

        if user is not None:
            # Filter the queryset for the 'category' field based on the logged-in user
            self.fields['category'].queryset = Category.objects.filter(owner=user)




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'state_or_region', 'whatsapp_number', 'phone_number', 'email', 'product', 'product_entry', 'address']

        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'phone_number': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'email': forms.EmailInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'address': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'product': forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'product_entry': forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

    state_or_region = forms.ModelChoiceField(
        queryset=Region.objects.none(),  # Empty initially, will be filled dynamically based on country selection
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'id': 'state_or_region',  # Add an ID for JavaScript targeting
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        country_id = kwargs.pop('country_id', None)  # Extract country_id to filter regions
        country_name = kwargs.pop('country_name', None)  # Extract country_name to filter regions
        super(OrderForm, self).__init__(*args, **kwargs)

        if country_id or country_name:
            # Populate the queryset of state_or_region based on selected country
            if country_id:
                self.fields['state_or_region'].queryset = Region.objects.filter(country_id=country_id)
            elif country_name:
                try:
                    country = Country.objects.get(name__iexact=country_name)
                    self.fields['state_or_region'].queryset = Region.objects.filter(country=country)
                except Country.DoesNotExist:
                    self.fields['state_or_region'].queryset = Region.objects.none()



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']