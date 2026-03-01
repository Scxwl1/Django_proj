from django import forms
from .models import Product, Category, Manufacturer, Supplier, Unit
from .models import Order, OrderItem, Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'status', 'pickup_point', 'issue_date', 'user']
        widgets = {
            'issue_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['article', 'name', 'category', 'description', 'manufacturer', 
                  'supplier', 'price', 'unit', 'quantity_in_stock', 'discount', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['manufacturer'].queryset = Manufacturer.objects.all()
        self.fields['supplier'].queryset = Supplier.objects.all()
        self.fields['unit'].queryset = Unit.objects.all()
        if self.instance and self.instance.pk:
            self.fields['article'].disabled = True