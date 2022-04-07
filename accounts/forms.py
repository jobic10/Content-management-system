from dataclasses import fields
<<<<<<< HEAD
from django.forms import ModelForm, widgets
from .models import Order, CustomUser
=======
from xml.dom import ValidationErr
from django.forms import EmailField, ModelForm, widgets
from .models import Order,CustomUser
>>>>>>> db3adf6 (error in forms.py)
from django import forms
from django.contrib.auth.hashers import make_password


class FormSetting(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormSetting, self).__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class Create_Order(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CustomUserForm(FormSetting):
<<<<<<< HEAD

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
=======
    first_name=forms.CharField(max_length=100,label="First Name")
    last_name=forms.CharField(max_length=100,label="Last Name")
    email=forms.EmailField(required=True)
    password=forms.CharField(widget=forms.PasswordInput,required=True)
    password2=forms.CharField(widget=forms.PasswordInput,required=True)
    widget={
        'password':forms.PasswordInput(),
        'password2':forms.PasswordInput()
    }


    def __init__(self, *args, **kwargs):
        super(CustomUserForm,self).__init__(*args,**kwargs)
>>>>>>> db3adf6 (error in forms.py)
        if kwargs.get('instance'):
            instance = kwargs.get('instance').__dict__
            self.fields['password'].required = False

            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
<<<<<<< HEAD
                self.fields['password'].widget.attrs['placeholder'] = "Enter your Password"
=======
                self.fields['password'].widget.attrs['placeholder']= "Enter your Password"

>>>>>>> db3adf6 (error in forms.py)
            else:
                self.fields['first_name'].required = True
                self.fields['last_name'].required = True

    def clean_email(self, *args, **kwargs):
<<<<<<< HEAD
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError(
                        "The given email is already registered")
        return formEmail

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
=======
        FormEmail=self.cleaned_data['email'].lower()
        if self.instance.pk is None:            #insert
            if CustomUser.objects.filter(email=FormEmail).exists():
                raise forms.ValidationError('The Given mail is already registered')
        else:
            DbEmail=self.Meta.model.objects.get(id=self.instance.pk).email.lower()
            if DbEmail != FormEmail:
                if CustomUser.objects.filter(email=FormEmail).exists():
                    raise forms.ValidationError("the given email is already Registered")
        return FormEmail


    def clean_password(self):
        
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')
        print(password)
        print(password2)
        if password is None:
            raise forms.ValidationError('password required')
        if password != password2:        
            raise forms.ValidationError('Password Mismatch')
>>>>>>> db3adf6 (error in forms.py)
        if self.instance.pk is None:
            if not password:
                return self.instance.password
        return make_password(password)

<<<<<<< HEAD
=======
       

    

   
>>>>>>> db3adf6 (error in forms.py)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
