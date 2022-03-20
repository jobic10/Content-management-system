from dataclasses import fields
from django.forms import ModelForm, widgets
from .models import Order,CustomUser
from django import forms
from django.contrib.auth.hashers import make_password 


class FormSetting(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(FormSetting,self).__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs['class']='form-control'


class Create_Order(ModelForm):
    class Meta:
        model=Order
        fields='__all__'

class CustomUserForm(FormSetting):

    email=forms.EmailField(required=True)
    password=forms.CharField(widget=forms.PasswordInput)
    widget={
        'password':forms.PasswordInput(),
    }


    def __inti__(self, *args, **kwargs):
        super(CustomUserForm,self).__init__(*args,**kwargs)
        if kwargs.get('instance'):
            instance=kwargs.get('instance').__dict__
            self.fields['password'].required=False
            
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial=instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder']= "Enter your Password"
            else:
                self.fields['first_name'].required=True
                self.fields['last_name'].required=True

    def clean_email(self, *args, **kwargs):
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
        password = self.cleaned_data.get('password',None)
        if self.instance.pk is None:
            if not password:
                return self.instance.password
        return make_password(password)

    
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','password']



