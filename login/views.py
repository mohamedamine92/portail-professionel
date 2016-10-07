#-*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from login.forms import *
from models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from random import randint
from django.core.urlresolvers import reverse
from datetime import time, tzinfo
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from time import strptime

def home(request):
	spec=Specialite.objects.all()
	s_spec=S_specialite.objects.all()
	return render(request, 'home/index.html',locals())


def profsignup(request):
    spec=Specialite.objects.all() 
    if request.is_ajax():
        counter=request.POST['counter']
        s_spec=S_specialite.objects.filter(categorie=counter)
        template = "home/ajax1.html"
        return render_to_response(template,{'counter': counter ,'s_spec':s_spec},context_instance=RequestContext(request))
    if request.method == 'POST':  # S'il s'agit d'une requ?te POST
        form = ProfForm(request.POST)
        if form.is_valid(): 
              # Nous reprenons les donn?es Categorie.objects.get(id=form.cleaned_data['categorie'])
            user = User.objects.create_user(first_name=form.cleaned_data['nom'],
            last_name=form.cleaned_data['prenom'],
            email=form.cleaned_data['email'],
            username=form.cleaned_data['login'],
            password=form.cleaned_data['mdp'])
            signup=Prof(type=form.cleaned_data['type'],user=user,
            spec=form.cleaned_data['spec'],
            code=randint(12578,12778),
            ); signup.save() 
            subject="welcome to link" ; message="Hello "+signup.user.first_name+" thank you for the registration please verify your account with this secret code :"+str(signup.code)
            from_email=settings.EMAIL_HOST_USER ; to_list=[signup.user.email] 
            send_mail(subject,message,from_email,to_list,fail_silently=False) 
            '''username = signup.user.username
            password =  signup.user.password
            user1 = authenticate(username=username, password=password) ; login(request, user1)  '''
            connect(request)
            return redirect (reverse(verif_email))
    
    else: # Si ce n'est pas du POST, c'est probablement une requ?te GET
        form = ProfForm()  # Nous cr?ons un formulaire vide
    return render(request, 'home/hello.html', locals())

def clientsignup(request):
    if request.method == 'POST':  # S'il s'agit d'une requ?te POST
        form = ProfForm(request.POST)
        if form.is_valid(): 
            # Nous reprenons les donn?es Categorie.objects.get(id=form.cleaned_data['categorie'])
            user = User.objects.create_user(first_name=form.cleaned_data['nom'],
            last_name=form.cleaned_data['prenom'],
            email=form.cleaned_data['email'],
            username=form.cleaned_data['login'],
            password=form.cleaned_data['mdp'],
            )
            signup=Client(user=user,code=randint(12578,12778),); signup.save()

            subject="welcome to link" ; message="Hello "+signup.user.first_name+" thank you for the registration please verify your account by clicking that link"+str(signup.code)
            from_email=settings.EMAIL_HOST_USER ; to_list=[signup.user.email] 
            send_mail(subject,message,from_email,to_list,fail_silently=False)
            connect(request)
            return redirect (reverse(verif_email))
    
    else: # Si ce n'est pas du POST, c'est probablement une requ?te GET
        
        form = ProfForm()  # Nous cr?ons un formulaire vide
    return render(request, 'home/hello2.html', locals())


def connect(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['mdp']
            user = authenticate(username=username, password=password)
            if user:  
                
                login(request, user)  
                #prof=Prof.objects.get(user=user)
                if Prof.objects.filter(user=user): 
                    
                    prof=Prof.objects.get(user=user)
                    if prof.verification==False:                
                        return redirect (reverse(verif_email))
                    else:
                        return redirect (reverse(profile))
                else:
                    clt=Client.objects.get(user=user)
                    if clt.verification==False:                
                        return redirect (reverse(verif_email))
                    else:
                        return redirect(reverse(recherche))
                    
            else:
                error = True
    else:
        form = ConnexionForm()
    return render(request, 'home/loginFail.html', locals())

@login_required
def verif_email(request):
   
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            verif = form.cleaned_data['login']
           
            if Prof.objects.filter(user=request.user) :
                prof=Prof.objects.get(user=request.user)
                if verif==str(prof.code):
                    prof.verification=True ; prof.save()
                    return redirect (reverse(edit))
            else:
                clt=Client.objects.get(user=request.user)
                if verif==str(clt.code):
                    clt.verification=True ; clt.save() 
                    return redirect(reverse(profile_client))
    else:
        form = ConnexionForm()
    return render(request, 'home/email.html', locals())
    
@login_required
def profile(request):
    month=request.user.date_joined.strftime('%b')
    user=request.user
    prof=Prof.objects.get(user=user)
    return render(request, 'home/profile.html',locals())  
@login_required
def edit (request):
    gouve=Gouvernorat.objects.all()
    user=request.user
    prof=Prof.objects.get(user=user)


    if request.method == 'POST':  # S'il s'agit d'une requ?te POST
        form = update(request.POST)
        if form.is_valid(): 
            
            first_name=form.cleaned_data['nom']
            if first_name:
                user.first_name=first_name
            last_name=form.cleaned_data['prenom']
            if last_name:
                user.last_name=last_name
            noms=form.cleaned_data['noms']
            if noms and prof.type=='Société':
                prof.noms=noms
            mobile=form.cleaned_data['mobile']
            if mobile:
                prof.mobile=int(mobile)
            fixe=form.cleaned_data['fixe']
            if fixe:
                prof.fixe=int(fixe)
            fax=form.cleaned_data['fax']
            if fax:
                prof.fax=int(fax)
            
            lat=form.cleaned_data['lat']
            lon=form.cleaned_data['lon']
            adresse=form.cleaned_data['dele']
            if adresse and lat:
                if prof.adresse:
                        adr=Adresse.objects.get(id=prof.adresse.id)
                        adr.dele=adresse
                        adr.lat=lat
                        adr.lon=lon
                else:
                        adr=Adresse()
                        adr.dele=adresse
                        adr.lat=lat
                        adr.lon=lon
                adr.save()
                prof.adresse=adr
           
            desc=form.cleaned_data['desc']
            if desc:
                prof.desc=desc
            
            user.save();prof.save()
            return redirect (reverse(profile))
    
    else: # Si ce n'est pas du POST, c'est probablement une requ?te GET
        form = update()  # Nous cr?ons un formulaire vide
    return render(request, 'home/edit.html', locals())

def test2(request):


    counter = 0
    dele = []
    s_spec = []
    if request.is_ajax():
        bo = request.POST['bo']
        counter = request.POST['counter']
        if bo == "0":
            s_spec = S_specialite.objects.filter(categorie=counter)
            template = "home/ajax2.html"
        else:
            dele = Delegation.objects.filter(gouv=counter)
            template = "home/ajax.html"

        return render_to_response(template, {'dele': dele, 's_spec': s_spec}, context_instance=RequestContext(request))
    
    
def test(request):
	
    logout(request)
    #k=request.session['my_key']
    return redirect (reverse(home),locals())
    
@login_required
def recherche (request):
    spec=Specialite.objects.all()
    gouve=Gouvernorat.objects.all()
    user=request.user
    prof=Client.objects.get(user=user)
    queryset_list = []
    client=True
    query=request.GET.get("gouv")
    query1=request.GET.get("dele")
    query2=request.GET.get("spec")
    query3=request.GET.get("s_spec")

    if query:
        queryset_list = Prof.objects.filter(adresse__dele=query1,spec=query3)

    paginator = Paginator(queryset_list, 1)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
       # "prof":prof,
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "gouve":gouve,
        "spec":spec,
        "client":client
    }
    return render(request, 'home/recherche.html',context)

def profile_client(request):

    return render(request,"home/profile_client.html",{})


def cli_mail(request):
    client = get_object_or_404(Client, user_id=request.user.id)
    # prof=Prof.objects.filter(user_id=request.user.id)
    id_user = client.id
    query = discussion.objects.filter(cli_id=id_user)
    context={
        "query":query,

    }

    return render(request,"home/mailbox_cli.html",context)

def cli_msgs(request,id=None):
    #instance = get_object_or_404(discussion, id=id)
    query = msg.objects.filter(discuss_id=id)
    client = True
    form = msg_reply(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cont = form.data['contenu']
            msg(contenu=cont, prop_id=request.user.id, discuss_id=id).save()

    else:
        form = msg_reply()

    context = {
        "query": query,
        "id": request.user.id,
        "client":client

    }

    return render(request,"home/msg_cli.html",context)


def view_prof(request,id=None):
    prof=get_object_or_404(Prof,id=id)
    client=get_object_or_404(Client,user_id=request.user.id)
    form = MessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cont = form.data['contenu']

            # clien=get_object_or_404(Client,user_id=idcli)
            disc = discussion(profes_id=id, cli_id=client.id, state=0)
            disc.save()
            msg(contenu=cont, discuss_id=disc.id, prop_id=request.user.id).save()
    else:
        form = MessageForm()
    context={

        "prof":prof,
        "form": form,

    }
    return render(request,"home/view_prof.html",context)
#liste de discussions du professionnel
def prof_mail(request):
    prof = get_object_or_404(Prof, user_id=request.user.id)
    # prof=Prof.objects.filter(user_id=request.user.id)
    id_user = prof.id
    client=False
    query = discussion.objects.filter(profes_id=id_user)
    context={
        "query":query,
        "client":client

    }

    return render(request,"home/mailbox_prof.html",context)

def prof_msgs(request,id=None):
    #instance = get_object_or_404(discussion, id=id)
    query = msg.objects.filter(discuss_id=id)
    form = msg_reply(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cont = form.data['contenu']
            msg(contenu=cont, prop_id=request.user.id, discuss_id=id).save()

    else:
        form = msg_reply()

    context = {
        "query": query,
        "id": request.user.id,

    }

    return render(request,"home/msg_prof.html",context)

def recherche_h (request):
    spec=Specialite.objects.all()
    gouve=Gouvernorat.objects.all()

    queryset_list = []

    query=request.GET.get("gouv")
    query1=request.GET.get("dele")
    query2=request.GET.get("spec")
    query3=request.GET.get("s_spec")

    if query:
        queryset_list = Prof.objects.filter(adresse__dele=query1,spec=query3)

    paginator = Paginator(queryset_list, 1)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
       # "prof":prof,
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "gouve":gouve,
        "spec":spec,
    }
    return render(request, 'home/recherche_h.html',context)

def view_prof_h(request,id=None):
    prof=get_object_or_404(Prof,id=id)



    context={

        "prof":prof,


    }
    return render(request,"home/viw_prof_h.html",context)

def send_devis(request,id=None):
    instance = get_object_or_404(Prof, id=id)
    form1 = DevisForm(request.POST)
    client = get_object_or_404(Client, user_id=request.user.id)
    if request.method == 'POST':
        if form1.is_valid():
            cont = form1.data['services']
            id = form1.data['id']
            dev = devis(profess_id=id, cli_id=client.id, notif=1)
            dev.save()
            list = cont.split('#')
            list = filter(None, list)
            for index in list:
                serv = index
                service(cont_service=serv, prix=0, devis_id=dev.id).save()

                # if cont == "":
                # print cont
    else:
        form1 = DevisForm()

    context = {
        "form": form1,
        "instance":instance

    }
    return render(request,'home/send_devis.html',context)

def devis_prof(request):
    prof = get_object_or_404(Prof, user_id=request.user.id)
    # prof=Prof.objects.filter(user_id=request.user.id)
    id_user = prof.id
    query = devis.objects.filter(profess_id=id_user)
    context = {
        "query": query,


    }
    return render(request,'home/devis_prof.html',context)

def devis_prof_det(request,id=None):
    instance = get_object_or_404(devis, id=id)
    query = service.objects.filter(devis_id=instance.id)
    client=False

    context = {
        "query": query,
        "client": client


    }
    return render(request, "home/devis_prof_detail.html", context)
#client propose rendez_vous
def fix_rendez_vous(request,id=None):
    client = get_object_or_404(Client, user_id=request.user.id)
    if request.method == 'POST':

        form = rendez_vousForm(request.POST)

        if form.is_valid():
            t = 1
            date = form.data['date']
            time = form.data['time']

            rendez_vous(profess_id=id, cli_id=client.id, date=date, time=time, state=0).save()



    else:
        t=0
        form = rendez_vousForm()



    return render(request,"home/fix_rendez_vous.html",locals())
#professionnel rendez_vous
def prof_rendez_vous(request):
    prof=get_object_or_404(Prof,user_id=request.user.id)
    query=rendez_vous.objects.filter(profess_id=prof.id,state=0)




    return render(request,"home/prof_rendez_vous.html",locals())
#prof confirme rendez_vous
def confirm_rend(request,id=None):
    rend=get_object_or_404(rendez_vous,id=id)
    rend.state=1
    rend.save()
    messages.success(request, "Successfully confirmed")

    return redirect (reverse(prof_rendez_vous))
#prof delete rendez_vous
def delete_rend(request,id=None):
    rend=get_object_or_404(rendez_vous,id=id)
    rend.delete()
    return redirect(reverse(prof_rendez_vous))
#client rendez_vous
def cli_rend(request):
    client=get_object_or_404(Client,user_id=request.user.id)
    query=rendez_vous.objects.filter(cli_id=client.id)

    return render(request,"home/cli_rendez_vous.html",locals())




