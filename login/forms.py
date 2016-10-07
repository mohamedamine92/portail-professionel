#-*- coding: utf-8 -*-
from django import forms
from models import *
from django.contrib.auth.models import User
class ProfForm(forms.ModelForm):
    
	nom =forms.CharField(max_length=100 ,required=True)
	prenom =forms.CharField(max_length=100 ,required=True)
	email =forms.EmailField(max_length=254  ,required=True)
	login =forms.CharField(max_length=50 ,required=True)
	mdp =forms.CharField(max_length=100 ,required=True)
	
	class Meta:
		model = Prof
		fields = ('spec','type')	
	
	def clean_login(self):
		login=self.cleaned_data['login']
		if User.objects.filter(username=self.cleaned_data['login']):
			raise forms.ValidationError("this login is already taken")
		return login
	def clean_email(self):
		email=self.cleaned_data['email']
		if User.objects.filter(email=email):
			raise forms.ValidationError("there is an existent account with the same email")
		return email 

class ConnexionForm(forms.Form):
	
    login=forms.CharField(max_length=50 ,required=True)
    mdp =forms.CharField(max_length=100 ,required=True)
class update(forms.ModelForm):
    
    nom =forms.CharField(max_length=100 ,required=False)
    prenom =forms.CharField(max_length=100 ,required=False)
    noms =forms.EmailField(max_length=254  ,required=False)
    mobile =forms.IntegerField(required=False)
    fixe =forms.IntegerField(required=False)
    fax=forms.IntegerField(required=False)
    lon =forms.CharField(max_length=100 ,required=False)
    lat =forms.CharField(max_length=100 ,required=False)
    desc=forms.CharField(widget=forms.Textarea ,required=False)
    class Meta:
        model=Adresse
        fields =('dele',)
class recherche (forms.ModelForm) :
    spec=forms.CharField(max_length=15 ,required=False)
    gouv=forms.CharField(max_length=15 ,required=False)
    s_spec=forms.CharField(max_length=15 ,required=False)
    class Meta:
        model=Adresse
        fields =('dele',)

class MessageForm(forms.Form):
    class Meta:
        model = msg
        fields = ('contenu')

class msg_reply(forms.Form):
    class Meta:
        model = msg
        fields = ('contenu')

class DevisForm(forms.Form):
    class Meta:
        model=service
        fields=('cont_service')


class rendez_vousForm(forms.Form):
    class Meta:
        model=rendez_vous
        fields=('date','time')
