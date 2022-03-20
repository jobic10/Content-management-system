from email import message
from telnetlib import STATUS
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from random import randint
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from .email_backend import EmailBackend
from django.contrib import messages
from django.contrib.auth import logout,login



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

def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type=='1':
            return redirect('dashboard')

    if request.method=="POST":
        user=EmailBackend.authenticate(request,username=request.POST.get('email'),password=request.POST.get('password'))
        if user!=None:
            login(request,user)
            if user.user_type == '1':
                return redirect('dashboard')

        else:
            messages.error(request,'Invalid Login Parameters')
            return redirect('/')
        
    context={}
    return render(request,'login.html',context)

def account_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Thanks for Checking on CMS Goodbye!!")
        return redirect('login')

    else:
        messages.error(request,"You need to Login to be able to accsss this Software")
        return redirect('login')
    



def register(request):
    userForm=CustomUserForm(request.POST or None)
    if request.method=='POST':
        if userForm.is_valid():
            user=userForm.save(commit=False)
            user.cms=user
            user.save()
            messages.success(request,'Account Created Successfully.You can now login')
            return redirect('login')
        else:
            messages.error(request,"Provided data Failed Validation")
    

   
    context={
        'form':userForm
    }
    return render(request,'register.html',context)



    
    
        

