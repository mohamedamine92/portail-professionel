from random import randint
from django.conf.urls import url
from . import views
pat='^prof_signup'+str(randint(5247,5345))+'$'
pat1='^client_signup'+str(randint(5247,5345))+'$'

urlpatterns = [
   
    url(r'^home$', views.home), 
    url(pat, views. profsignup),
    url(pat1 , views.clientsignup),
    url(r'^loginFail$', views.connect),
    url(r'^test$', views.test),
    url(r'^email_verif$', views.verif_email),
    url(r'^profile$', views.profile),#profile professionnel
    url(r'^edit$', views.edit),
    url(r'^test2$', views.test2),
    url(r'^recherche$',views.recherche),#recherche client connecte
    url(r'^recherche_h$', views.recherche_h),
    url(r'^cli_profile$', views.profile_client),
    url(r'^prof_devis$', views.devis_prof),#liste des devis du prof
    url(r'^prof_devis/(?P<id>\d+)/$', views.devis_prof_det,name="detail_devis"),#detail devis prof
    url(r'^cli_mail$', views.cli_mail),
    url(r'^devis/(?P<id>\d+)/$', views.send_devis,name="devis"),
    url(r'^prof_mail$', views.prof_mail),#liste des discussions du professionnel
    url(r'^cli_msgs/(?P<id>\d+)/$', views.cli_msgs,name='detail_disc'),
    url(r'^prof_msgs/(?P<id>\d+)/$', views.prof_msgs, name='detail_disc_prof'),#messages du prof
    url(r'^view_prof/(?P<id>\d+)/$', views.view_prof,name='detail'),
    url(r'^view_prof_h/(?P<id>\d+)/$', views.view_prof_h, name='detail_h'),
    url(r'^rendez_vous/(?P<id>\d+)/$', views.fix_rendez_vous, name='rend'),
    url(r'^rendez_vous_prof$',views.prof_rendez_vous),
    url(r'^confirm/(?P<id>\d+)/$', views.confirm_rend, name='confirm'),
    url(r'^delete/(?P<id>\d+)/$', views.delete_rend, name='del'),
    url(r'^rendez_vous$', views.cli_rend),



	
    ]