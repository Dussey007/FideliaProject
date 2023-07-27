from collections import UserList
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from urllib import request
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.utils.http import urlencode
from django.db.models import Q, Exists
from django.db.models.deletion import ProtectedError
from account.forms import EditProfileForm, GradeForms, PasswordChangingForm, SignUpForm, SignupForms, CategorieForms, \
    SouscrireForms, ProduitForms, RelanceForms
from account.models import Client, Grade, Produit, Categorie, Souscrire, User, Relance


################################################
#
# 
# Fonction pour afficher les vues
#
# 
###############################################


@login_required(login_url='login_view')
def home_view(request):
    nbre = Souscrire.objects.filter(employe_id=request.user.pk, souscription="En attente").count()  # En attente
    nbreClS = Souscrire.objects.filter(employe_id=request.user.pk, souscription="Réalisé").count()  # réalisé
    nbreClNS = Souscrire.objects.filter(employe_id=request.user.pk, souscription="Non réalisé").count()  # Non réalisé

    return render(request, 'userss/message.html', {"nbre": nbre, "nbreClS": nbreClS, "nbreClNS": nbreClNS})  # vrai



def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Mot de passe modifié avec succes!!")
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'userss/change-password.html', {"form": form})
    else:
        return redirect('login_view')


@login_required(login_url='login_view')
def ajouter_view(request):
    Clients = Client.objects.all().filter(employe_id=request.user.pk)
    form = SignupForms(user=request.user)

    if 'recherche' in request.GET:
        name = request.GET['recherche']
        Clients = Client.objects.filter(
            Q(nom__icontains=name) | Q(profil__icontains=name) | Q(nomGrade__nomGrade__icontains=name),
            employe_id=request.user.pk).order_by('-id')
    else:
        Clients = Client.objects.filter(employe_id=request.user.pk).all().order_by('-id')

    paginator = Paginator(Clients, 8)  # Show 4 contacts per page

    page_list = request.GET.get('page', 8)
    page = paginator.get_page(page_list)

    context = {
        'page': page,
        "form": form,
    }

    return render(request, 'GesClient/ajouter.html', context)


@login_required(login_url='login_view')
def bases_view(request):
    nbre = Client.objects.all().count()
    return render(request, 'GesClient/base.html', {"nbre": nbre})


###########################################################################
#
#
# Fonctions pour afficher les listes et faire des recherches dans ces listes
#
# 
###########################################################################


@login_required(login_url='login_view')
def searchSous_view(request):
    search = request.GET.get('recherche')

    context = {
        'search': search,
    }
    return render(request, 'GesClient/souscrire.html', context)


# Page propositions
@login_required(login_url='login_view')
def liste_view(request):
    if 'recherche' in request.GET:
        name = request.GET['recherche']
        Clients = Client.objects.filter(employe_id=request.user.pk).filter(
            Q(nom__icontains=name) | Q(profil__icontains=name)).order_by('-id')


    else:
        Clients = Client.objects.filter(employe_id=request.user.pk).order_by('-id')

    paginator = Paginator(Clients, 8)  # Show 4 contacts per page

    page_list = request.GET.get('page', 8)
    page_object = paginator.get_page(page_list)


    context = {
        'clients': page_object,
    }
    return render(request, 'GesClient/liste.html', context)


@login_required(login_url='login_view')
def souscrires_view(request):
    form = SouscrireForms()


    if 'recherche' in request.GET:
        name = request.GET['recherche']
        clients = None
        Souscrires = Souscrire.objects.filter(client__nom__icontains=name).filter(employe_id=request.user.pk)


    elif request.method == "POST":
        Souscrires = Souscrire.objects.filter(employe_id=request.user.pk).order_by('-id')
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        select = request.POST.get('selection')

        if select == "echeance":
            Souscrires = Souscrire.objects.filter(employe_id=request.user.pk).filter(date_echeance__gte=fromdate,
                                                                                     date_echeance__lte=todate)
        elif select == "effet":
            Souscrires = Souscrire.objects.filter(employe_id=request.user.pk).filter(date_effet__gte=fromdate,
                                                                                     date_effet__lte=todate)
        elif select == "emission":
            Souscrires = Souscrire.objects.filter(employe_id=request.user.pk).filter(date_emission__gte=fromdate,
                                                                                     date_emission__lte=todate)
        else:
            messages.warning(request, "Faites un bon choix !!")

    else:
        Souscrires = Souscrire.objects.filter(employe_id=request.user.pk).order_by('-id')
    paginator = Paginator(Souscrires, 8)

    page_number = request.GET.get('page', 8)
    page_object = paginator.get_page(page_number)

    clients = Client.objects.filter(employe_id=request.user.pk)

    context = {
        "form": form,
        "Souscrires": page_object,
        "clients": clients

    }

    return render(request, 'GesClient/souscrire.html', context)


@login_required(login_url='login_view')
def grade_view(request):
    form = GradeForms()
    if 'recherche' in request.GET:
        name = request.GET['recherche']
        Grades = Grade.objects.filter(nomGrade__icontains=name).order_by('-id')
    else:
        Grades = Grade.objects.order_by('-id')
    paginator = Paginator(Grades, 3)

    page_number = request.GET.get('page', 3)
    page_object = paginator.get_page(page_number)

    context = {
        "form": form,
        "Grade": page_object,

    }

    return render(request, 'GesClient/grade.html', context)


@login_required(login_url='login_view')
def registerss_view(request):
    form = SignUpForm()
    return render(request, 'accountss/register.html', {"form": form})


@login_required(login_url='login_view')
def categorie_view(request):
    formCat = CategorieForms()

    if 'recherche' in request.GET:
        name = request.GET['recherche']
        Categories = Categorie.objects.filter(employe_id=request.user.pk, nomCategorie__icontains=name).order_by('-id')
    else:
        Categories = Categorie.objects.all().order_by(
            '-id')  # i=(Majuscule ou miniscule) contains =(affiche tout même juste une partie)

    paginator = Paginator(Categories, 3)  # Show 4 contacts per page

    page_list = request.GET.get('page', 3)
    page_object = paginator.get_page(page_list)

    context = {
        "form": formCat,
        'Categories': page_object,
    }

    return render(request, 'GesClient/categorie.html', context)


@login_required(login_url='login_view')
def produit_view(request):
    form = ProduitForms()
    if 'recherche' in request.GET:
        name = request.GET['recherche']
        Produits = Produit.objects.filter(nomProduit__icontains=name).order_by('-id')
    else:
        Produits = Produit.objects.all().order_by(
            '-id')  # i=(Majuscule ou miniscule) contains =(affiche tout même juste une partie)

    paginator = Paginator(Produits, 3)  # Show 4 contacts per page

    page_list = request.GET.get('page', 3)
    page_object = paginator.get_page(page_list)

    context = {
        "form": form,
        'Produits': page_object,
    }

    return render(request, 'GesClient/produit.html', context)


# Liste des clients confirmé

@login_required(login_url='login_view')
def listeConfirme_view(request):
    nbreClS = Souscrire.objects.filter(employe_id=request.user.pk, souscription="Réalisé").all()

    form = SignupForms(user=request.user)

    paginator = Paginator(nbreClS, 5)  # Show 5 contacts per page

    page_list = request.GET.get('page', 5)
    page = paginator.get_page(page_list)

    context = {
        'page': page,
        "form": form,
    }

    return render(request, 'GesClient/listeConfirme.html', context)


#
#
#
#           SOLUTIONS   
#
#
#

@login_required(login_url='login_view')
def VPersonnelClient_view(request, ids):
    sous = Souscrire.objects.filter(souscription="Réalisé")
    Pclient = Client.objects.filter(Exists(sous), employe_id=ids)

    return render(request, 'GesClient/voirPersoClient.html', {'Pclients': Pclient})


@login_required(login_url='login_view')
def PersonnelClient_view(request):
    user = User.objects.get(id=1)
    Pclient = Client.objects.filter(employe_id=user)
    sous = Souscrire.objects.filter(Exists(Pclient), souscription="Réalisé")

    return render(request, 'GesClient/persoClient.html', {'Pclient': sous})


# Liste des propositions réalisés ou confirmés

@login_required(login_url='login_view')
def listeNonConfirme_view(request):
    nbreClN = Souscrire.objects.filter(employe_id=request.user.pk, souscription="Non réalisé").all()
    form = SignupForms(user=request.user)

    paginator = Paginator(nbreClN, 5)  # Show 5 contacts per page

    page_list = request.GET.get('page', 5)
    page = paginator.get_page(page_list)

    context = {
        'page': page,
        "form": form,
    }

    return render(request, 'GesClient/listeNonConfirme.html', context)


# lite propositions en attente
@login_required(login_url='login_view')
def listeEnAttente_view(request):
    nbreAttente = Souscrire.objects.filter(employe_id=request.user.pk, souscription="En attente").all()
    form = SignupForms(user=request.user)

    paginator = Paginator(nbreAttente, 5)  # Show 5 contacts per page

    page_list = request.GET.get('page', 5)
    page = paginator.get_page(page_list)

    context = {
        'page': page,
        "form": form,
    }

    return render(request, 'GesClient/listeEnAttente.html', context)


@login_required(login_url='login_view')
def listePersonnel_view(request):

    if 'recherche' in request.GET:
        name = request.GET['recherche']
        nbreEmpl = User.objects.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name)).order_by('-id')
    else:
        nbreEmpl = User.objects.all().order_by('-id')

    paginator = Paginator(nbreEmpl, 8)  # Show 4 contacts per page

    page_list = request.GET.get('page', 8)
    page_object = paginator.get_page(page_list)

    context = {
        'nbreEmpl': page_object,
    }

    return render(request, 'GesClient/listePersonnel.html', context)


################################################
#
# 
# Fonctions POUR AFFICHER LES VUES
#
# 
###############################################


@login_required(login_url='login_view')
def param_view(request):  # MODIFICATION DU COMPTE DE L4UTILISATEUR
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employe = request.user
            obj.save()
            messages.success(request, "Compte modifié avec succes!!")
        else:
            messages.error(request, "Informations non valides!!")

    else:
        form = EditProfileForm(instance=request.user)

    if request.user.is_authenticated:
        if request.method == "POST":
            form2 = PasswordChangingForm(user=request.user, data=request.POST)
            if form2.is_valid():
                form2.save()
                update_session_auth_hash(request, form2.user)
                messages.success(request, "Mot de passe modifié avec succes!!")
            else:
                messages.error(request, "Informations non valides!!")
        else:
            form2 = PasswordChangingForm(user=request.user)

    context = {
        'form': form,
        'form2': form2,
    }

    return render(request, 'GesClient/param.html', context)


@login_required(login_url='login_view')
def affModifMsg_view(request):
    return render(request, "message/msgMod.html")


@login_required(login_url='login_view')
def affErrorEnrgMsg_view(request):
    return render(request, "message/ErrorEnrg.html")


@login_required(login_url='login_view')
def affErrorMsgDate_view(request):
    return render(request, "message/messagedate.html")


@login_required(login_url='login_view')
def affSupMsg_view(request):
    return render(request, "message/msgSup.html")


@login_required(login_url='login_view')
def affEnrgMsg_view(request):
    return render(request, "message/EnrgMsg.html")


@login_required(login_url='login_view')
def affErrorMsg_view(request):
    return render(request, "message/error.html")


################################################
#
# 
# FONCTIONS POUR MODIFIER , SUPPRIMER , ET VOIR
#
# 
###############################################


#
#
#################################################################################
#
#
#            FONCTIONS DE SUPPRESSIONS
#
#
################################################################################ 
#
#


@login_required(login_url='login_view')
def deleteClient_view(request, id):
    if request.method == "POST":
        pi = Client.objects.get(pk=id)
        try:
            pi.delete()
            messages.success(request, "Client supprimé avec succes!!")
        except ProtectedError:
            messages.warning(request, "Ce Client ne peut être supprimé car il a souscrit à une assurance!!")
        return redirect('ajouter')


@login_required(login_url='login_view')
def deleteRelance_view(request, id):
    if request.method == "POST":
        pi = Relance.objects.get(pk=id)
        pi.delete()
        messages.success(request, "Client supprimé avec succès!!")
        return redirect('import_data')




@login_required(login_url='login_view')
def deleteGrade_view(request, id):
    if request.method == "POST":
        pi = Grade.objects.get(pk=id)
        try:
            pi.delete()
            messages.success(request, "Grade supprimé avec succes!!")
        except ProtectedError:
            messages.warning(request, "Ce grade ne peut être supprimé car déjà utilisé!!")
        return redirect('grade')


@login_required(login_url='login_view')
def deleteSouscription_view(request, id):
    if request.method == "POST":
        pi = Souscrire.objects.get(pk=id)
        pi.delete()
        messages.success(request, "Proposition supprimé avec succes!!")
        return redirect('souscrire')
        # return redirect('msgSup')


@login_required(login_url='login_view')
def deleteCategorie_view(request, id):
    if request.method == "POST":
        pi = Categorie.objects.get(pk=id)
        try:
            pi.delete()
            messages.success(request, "Categorie supprimé avec succes!!")
        except ProtectedError:
            messages.warning(request, "Cette catégorie ne peut être supprimé car déjà utilisé!!")
        return redirect('categorie')


@login_required(login_url='login_view')
def deleteProduit_view(request, id):
    if request.method == "POST":
        pi = Produit.objects.get(pk=id)
        pi.delete()
        messages.success(request, "Produit supprimé avec succes!!")
        return redirect('produit')


@login_required(login_url='login_view')
def deleteRelance_view(request, id):
    if request.method == "POST":
        pi = Relance.objects.get(pk=id)
        pi.delete()
        messages.success(request, "Relance supprimé avec succes!!")
        return redirect('import-data')


@login_required(login_url='login_view')
def deleteUser_view(request, id):
    if request.method == "POST":
        pi = User.objects.get(pk=id)
        try:
            pi.delete()
            messages.success(request, "Utilisateur supprimé avec succes!!")
            return redirect('personnel')
        except ProtectedError:
            messages.warning(request, "Cet utilisateur ne peut être supprimé car a enregistré des souscriptions")
        return redirect('personnel')


#
#   
##################################################################################
#
#
#           FONCTIONS DE MODIFICATIONS
#
#
##################################################################################
#
#

# Client


@login_required(login_url='login_view')
def updateClient_view(request, id):
    if request.method == 'POST':
        pi = Client.objects.get(pk=id)
        fm = SignupForms(request.POST, instance=pi, user=request.user)
        if fm.is_valid():
            obj = fm.save(commit=False)
            obj.employe = request.user
            obj.save()
            messages.success(request, "Client modifié avec succes!!")
            return redirect('ajouter')
    else:
        pi = Client.objects.get(pk=id)
        fm = SignupForms(instance=pi, user=request.user)
    return render(request, 'operations/updateClient.html', {'form': fm})


# Grade

@login_required(login_url='login_view')
def updateGrade_view(request, id):
    if request.method == 'POST':
        pi = Grade.objects.get(pk=id)
        fm = GradeForms(request.POST, instance=pi)
        if fm.is_valid():
            obj = fm.save(commit=False)
            obj.employe = request.user
            obj.save()
            messages.success(request, "Grade modifié avec succes!!")
            return redirect('grade')
    else:
        pi = Grade.objects.get(pk=id)
        fm = GradeForms(instance=pi)
    return render(request, 'operations/updateGrade.html', {'form': fm})

    # Souscription


@login_required(login_url='login_view')
def updateSouscription_view(request, id):
    if request.method == 'POST':
        pi = Souscrire.objects.get(pk=id)
        fm = SouscrireForms(request.POST, instance=pi)
        if fm.is_valid():
            obj = fm.save(commit=False)
            obj.employe = request.user
            obj.save()
            messages.success(request, "Proposition modifié avec succes!!")
            return redirect('souscrire')
    else:
        pi = Souscrire.objects.get(pk=id)
        fm = SouscrireForms(instance=pi)
    return render(request, 'operations/updateSouscription.html', {'form': fm})

    # Categorie


@login_required(login_url='login_view')
def updateCategorie_view(request, id):
    if request.method == 'POST':
        pi = Categorie.objects.get(pk=id)
        fm = CategorieForms(request.POST, instance=pi)
        if fm.is_valid():
            obj = fm.save(commit=False)
            obj.employe = request.user
            obj.save()
            messages.success(request, "Catégorie modifié avec succes!!")
            return redirect('categorie')
    else:
        pi = Categorie.objects.get(pk=id)
        fm = CategorieForms(instance=pi)
    return render(request, 'operations/updateCategorie.html', {'form': fm})

    # Produit


@login_required(login_url='login_view')
def updateProduit_view(request, id):
    if request.method == 'POST':
        pi = Produit.objects.get(pk=id)
        fm = ProduitForms(request.POST, instance=pi)
        if fm.is_valid():
            obj = fm.save(commit=False)
            obj.employe = request.user
            obj.save()
            messages.success(request, "Produit modifié avec succes!!")
            return redirect('produit')
    else:
        pi = Produit.objects.get(pk=id)
        fm = ProduitForms(instance=pi)
    return render(request, 'operations/updateProduit.html', {'form': fm})


# UPDATE LISTE IMPORTE
@login_required(login_url='login_view')
def updateRelance_view(request, id):
    dateJ= timezone.now()
    date1 = dateJ
    date2 = dateJ
    date3 = dateJ
    if request.method == 'POST':
        pi = Relance.objects.get(pk=id)
        fm = RelanceForms(request.POST, instance=pi)
        if fm.is_valid():
            obj = fm
            obj.save(commit=False)
            # if obj.cleaned_data['']
            obj.employe = request.user
            obj.save()
            messages.success(request, " Appel  enregistré avec succès!!")
            return redirect('import_data')
    else:
        pi = Relance.objects.get(pk=id)
        fm = RelanceForms(instance=pi)
        print(date1)
    context={
        'form':fm,
    }
    return render(request, 'operations/updateRelance.html',context)


##################################################################
#
#
# VOIR LES INFORMATIONS DU COMPTE UTILISATEUR
#
#
##################################################################


@login_required(login_url='login_view')
def voirCompteUser_view(request):
    args = {
        'user': request.user,
    }
    return render(request, 'operations/seeUser.html', args)


# VOIR CLIENT


@login_required(login_url='login_view')
def seeClient_view(request, id):
    pi = Client.objects.get(pk=id)

    context = {
        "pi": pi
    }

    return render(request, 'operations/seeClient.html', context)


# VOIR UTILISATEUR

@login_required(login_url='login_view')
def voirUser_view(request, id):
    pi = User.objects.get(pk=id)

    context = {
        "pi": pi
    }
    return render(request, 'operations/seeUser.html', context)


# VOIR PROPOSITIONS

@login_required(login_url='login_view')
def voirProposition_view(request, id):
    pi = Souscrire.objects.get(pk=id)

    context = {
        "pi": pi
    }
    return render(request, 'operations/seeProposition.html', context)


################################################
#
# 
# Fonctions pour changement d'informations
#
#
###############################################


# MODIFIER COMPTE UTILISATEUR

@login_required(login_url='login_view')
def updateCompte_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employe = request.user
            obj.save()
            messages.success(request, "Compte modifié avec succes!!")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'operations/profileUser.html', {'form': form})
