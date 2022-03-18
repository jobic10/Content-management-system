from telnetlib import STATUS
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from random import randint
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def dashboard(request):
    # x=[randint(1,12) for p in range(0,1)]
    customer=Customer.objects.all()
    orders=Order.objects.all()
    total_order=orders.count()
    customers=customer.count()
    orders_deliver=orders.filter(status='Delivered').count()
    orders_pending=orders.filter(status='Pending').count()

    context={
        # 'x':x,
        'customer':customer,
        'orders':orders,
        'total_order':total_order,
        'customers':customers,
        'orders_deliver':orders_deliver,
        'orders_pending':orders_pending
    }
    
    return render(request,'dashboard.html',context)

def customer(request,pk_id):
    try:
        customer=Customer.objects.get(id=pk_id)
        orders=customer.order_set.all()      #what does it do
        total_orders=orders.count()
        myFilter=OrderFilter(request.GET,queryset=orders)
        orders=myFilter.qs
    except:
        customer={}
        orders={}
        myFilter={}
        total_orders=""

    context={
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'myFilter':myFilter,
    }
    
    
    return render(request,'customer.html',context)

def product(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'products.html',context)

def orderform(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=2)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(instance=customer)
    # form=Create_Order(initial={'customer':customer})
    if request.method=="POST":
        formset=OrderFormSet(request.POST,instance=customer)
        # form=Create_Order(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
       
    context={
        'formset':formset
    }
    return render(request,'orderform.html',context)

def updates(request,pk):
    order=Order.objects.get(id=pk)  
    form=Create_Order(instance=order)
    if request.method=='POST':
        form=Create_Order(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')


    context={
        'form':form

    }
    return render(request,'orderform.html',context)

def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context={
        'item':order
    }
    return render(request,'delete.html',context)

def login(request):
    context={}
    return render(request,'login.html',context)

def register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save

   
    context={
        'form':form
    }
    return render(request,'register.html',context)



    
    
        

