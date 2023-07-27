from django.contrib import admin
from .models import User, Client, Relance
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .resources import RelanceResource

admin.site.register(User)

@admin.register(Client)
class Client(admin.ModelAdmin):
   class meta:
        list_display = ('nom', 'prenom', 'sexe', 'telephone', 'email')
# exclude = ('id',)
@admin.register(Relance)
class RelanceAdmin(ImportExportModelAdmin):
    resource_class = RelanceResource
    list_display = ('id', 'branche', 'categorie', 'clients', 'telephone', 'adresse', 'numero_police', 'date_effet', 'date_expiration', 'immatriculation', 'marque', 'prime_totale', 'apporteur')




