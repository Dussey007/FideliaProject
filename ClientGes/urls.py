"""ClientGes URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views 

#app_name = 'ClientGes'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('account/', include('account.urls')),
    path('do_liste/', include('tasks.urls')),
    path('ajouter/', views.ajouter_view, name='ajouter'),
    path('liste/', views.liste_view, name='liste'),
    path('grades/', views.grade_view, name='grade'),
    path('parametre/', views.param_view, name='parametre'),
    path('produit/', views.produit_view, name='produit'),
    path('categorie/', views.categorie_view, name='categorie'),
    path('souscrire/', views.souscrires_view, name='souscrire'),
    path('bases/', views.bases_view, name='bases'),
    path('Confirme/', views.listeConfirme_view, name='Confirme'),
    path('NonConfirme/', views.listeNonConfirme_view, name='NConfirme'),
    path('EnAttente/', views.listeEnAttente_view, name='EnAttente'),
    path('listePersonnel/', views.listePersonnel_view, name='personnel'),
    path('voirPropositions/<int:id>/', views.voirProposition_view, name='voirP'),
    path('voirCompte/', views.voirCompteUser_view, name='voir'),
    path('voirUser/<int:id>/', views.voirUser_view, name='voirU'),
    path('voirClientPersonnel/<int:ids>/', views.VPersonnelClient_view, name='Pclients'),
    path('ClientPersonnel/', views.PersonnelClient_view, name='clientsP'),
    path('updateRelance/<int:id>/', views.updateRelance_view, name='relanceUp'),

    
    
    #recherche
    path('searchSouscription/', views.searchSous_view, name='search'),
    

    
    #AFFICHAGE DES MESSAGES EN REPONSE
    path('messageModification/', views.affModifMsg_view, name='msg'),
    path('messageSupression/', views.affSupMsg_view, name='msgSup'),
    path('messageEnrg/', views.affEnrgMsg_view, name='msgEnrg'),
    path('messageErreur/', views.affErrorMsg_view, name='msgError'),
    path('messageErreurDate/', views.affErrorMsgDate_view, name='datemsg'),
    path('messageErreurEnregistrement/', views.affErrorEnrgMsg_view, name='ErrorEnrg'),


    
    #Supression 
    path('deleteCl/<int:id>/', views.deleteClient_view, name='deletedCl'),
    path('deleteRl/<int:id>/', views.deleteRelance_view, name='deletedRel'),
    path('deleteProd/<int:id>/', views.deleteProduit_view, name='deletedProd'),
    path('deleteS/<int:id>/', views.deleteSouscription_view, name='deletedS'),
    path('deleteCat/<int:id>/', views.deleteCategorie_view, name='deletedCat'),
    path('deleteUser/<int:id>/', views.deleteUser_view, name='deletedUser'),
    path('deleteGrade/<int:id>/', views.deleteGrade_view, name='deletedGrade'),
    path('deleteRelance/<int:id>/', views.deleteRelance_view, name='deletedRelance'),






    #modification
    path('updateCl/<int:id>/', views.updateClient_view, name='updateCl'),
    path('updateProd/<int:id>/', views.updateProduit_view, name='updateProd'),
    path('updateCat/<int:id>/', views.updateCategorie_view, name='updateCat'),
    path('updateS/<int:id>/', views.updateSouscription_view, name='updateS'),
    path('updateUser/', views.updateCompte_view, name='updateUser'),
    path('updateGrade/<int:id>/', views.updateGrade_view, name='updateGrade'),
    path('changepass/', views.user_change_pass, name='changepass'),
    
    #voir un client
    path('SeeClient/<int:id>/', views.seeClient_view, name='seeCl'),
    


]
