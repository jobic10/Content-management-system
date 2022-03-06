from django.forms import ModelForm
from .models import Order



class Create_Order(ModelForm):
    class Meta:
        model=Order
        fields='__all__'
