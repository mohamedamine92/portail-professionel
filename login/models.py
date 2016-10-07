from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class Prof(models.Model):
    type=models.CharField(max_length=30 , blank=True)
    user= models.OneToOneField(User)
	#nom =models.CharField(max_length=100)
    noms=models.CharField(max_length=100 , blank=True)
	#prenom =models.CharField(max_length=100)
    fixe =models.IntegerField(blank=True , null=True)
    mobile =models.IntegerField(blank=True , null=True )
    fax =models.IntegerField(blank=True , null=True)
	#email =models.EmailField(max_length=254 , unique=True , default="a@a.com")
	#login =models.CharField(max_length=50 , unique=True)
	#mdp =models.CharField(max_length=100)
    spec =models.ForeignKey('S_specialite',null=True , blank=True)
    image =models.ImageField(upload_to="Images/",null=True , blank=True)
    verification=models.BooleanField(default=False);code=models.IntegerField()
    desc = models.TextField(default="", blank=True)
    adresse=models.ForeignKey('Adresse',null=True , blank=True)

    def __str__(self):
        return "profil de {0}".format(self.id)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})

    def get_absolute_url1(self):
        return reverse("detail_h", kwargs={"id": self.id})

    def get_absolute_url2(self):
        return reverse("devis", kwargs={"id": self.id})

    def get_absolute_url3(self):
        return reverse("rend", kwargs={"id": self.id})

class Specialite(models.Model):
	categorie =models.CharField(max_length=100)
	def __str__(self):
		return  self.categorie
class S_specialite(models.Model):
	categorie=models.ForeignKey('Specialite',null=True , blank=True)
	s_categorie =models.CharField(max_length=100)
	def __str__(self):
		return  self.s_categorie


class Client(models.Model):
    
    user= models.OneToOneField(User)
	#nom=models.CharField(max_length=100)
	#prenom=models.CharField(max_length=100)
	#email=models.EmailField(max_length=254)
    tel=models.IntegerField(null=True, blank=True)
    verification=models.BooleanField(default=False);code=models.IntegerField(default=0)
	#login=models.CharField(max_length=50 ,null=True)
	#mdp=models.CharField(max_length=100 ,null=True)
    adresse=models.ForeignKey('Delegation',null=True , blank=True)
	
    def __str__(self):
        return "profil de {0}".format(self.id)


class Gouvernorat(models.Model):
    nomg=models.CharField(max_length=100)
    
    def __str__(self):
   	   return self.nomg

class Delegation(models.Model):
    nomd=models.CharField(max_length=100)
    gouv=models.ForeignKey('Gouvernorat',null=True , blank=True)
    def __str__(self):
   	   return self.nomd
class Adresse (models.Model):
    dele=models.ForeignKey('Delegation',null=True , blank=True)
    lon=models.CharField(max_length=100 , blank=True)
    lat=models.CharField(max_length=100 , blank=True)
    
    def __str__(self):
   	   return self.lon

class discussion(models.Model):
    profes=models.ForeignKey('Prof')
    cli=models.ForeignKey('Client')
    state=models.IntegerField()
    def __str__(self):
         return "discussion {0}".format(self.id)

    def get_absolute_url(self):
        return reverse("detail_disc", kwargs={"id": self.id})

    def get_absolute_url1(self):
        return reverse("detail_disc_prof", kwargs={"id": self.id})

class msg(models.Model):
    contenu=models.CharField(max_length=300)
    prop=models.ForeignKey(User)
    discuss=models.ForeignKey('discussion')
    date=models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name="Date de l'envoi de message")

    def __str__(self):
        return "message {0}".format(self.id)


class service(models.Model):
    cont_service=models.CharField(max_length=300)
    prix=models.DecimalField(max_digits=8, decimal_places=2)
    devis=models.ForeignKey('devis')

    def __str__(self):
        return "service n {0}".format(self.id)


class devis(models.Model):
    profess=models.ForeignKey('Prof')
    cli=models.ForeignKey('Client')
    notif=models.IntegerField(null=True)

    def __str__(self):
        return  "devis n {0}".format(self.id)

    def get_absolute_url(self):
        return reverse("detail_devis", kwargs={"id": self.id})

class rendez_vous(models.Model):
    profess=models.ForeignKey('Prof')
    cli=models.ForeignKey('Client')
    date = models.DateField(auto_now_add=False, auto_now=False, null=True)
    time = models.TimeField(auto_now_add=False, auto_now=False, null=True)
    state = models.IntegerField()

    def __str__(self):
        return "rendez vous n {0}".format(self.id)

    def get_absolute_url(self):
        return reverse("confirm", kwargs={"id": self.id})

    def get_absolute_url1(self):
        return reverse("del", kwargs={"id": self.id})