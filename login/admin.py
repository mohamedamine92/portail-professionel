from django.contrib import admin
from login.models import *



# Register your models here.
class ProfAdmin(admin.ModelAdmin):
    list_display = ('id','user_id', 'type', 'noms', 'fixe', 'spec', 'desc', 'adresse')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','tel','adresse')

class SpecAdmin(admin.ModelAdmin):
    list_display = ('id','categorie')

class S_specAdmin(admin.ModelAdmin):
    list_display = ('categorie','s_categorie')

class GouvAdmin(admin.ModelAdmin):
    list_display = ('id','nomg')

class DelegAdmin(admin.ModelAdmin):
    list_display = ('nomd','gouv')


class AdressAdmin(admin.ModelAdmin):
    list_display = ('dele','lon','lat')

class MsgsAdmin(admin.ModelAdmin):
    list_display = ('id','contenu','prop','discuss','date')

class DiscAdmin(admin.ModelAdmin):
    list_display = ('id', 'profes', 'cli', 'state')

class ServAdmin(admin.ModelAdmin):
    list_display = ('id', 'cont_service', 'prix', 'devis')

class DevAdmin(admin.ModelAdmin):
    list_display = ('id', 'profess', 'cli', 'notif')

class rendez_vousAdmin(admin.ModelAdmin):
    list_display = ('id','profess','cli','date','time','state')


admin.site.register(Prof,ProfAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Specialite,SpecAdmin)
admin.site.register(S_specialite,S_specAdmin)
admin.site.register(Gouvernorat,GouvAdmin)
admin.site.register(Delegation,DelegAdmin)
admin.site.register(Adresse,AdressAdmin)
admin.site.register(msg,MsgsAdmin)
admin.site.register(discussion,DiscAdmin)
admin.site.register(service,ServAdmin)
admin.site.register(devis,DevAdmin)
admin.site.register(rendez_vous,rendez_vousAdmin)





