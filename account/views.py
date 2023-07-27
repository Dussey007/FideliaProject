# from multiprocessing.connection import user
import csv
from datetime import date, datetime
from io import TextIOWrapper

from django.core.exceptions import ValidationError
from http.client import HTTPResponse
from django.contrib import messages
from time import strptime
from datetime import timedelta, datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings  # MAIL ENVOIE
from django.core.mail import send_mail  # MAIL ENVOIE
from django.utils.datastructures import MultiValueDictKeyError
from tablib import Dataset
from account.resources import RelanceResource

from django.shortcuts import render, redirect
from account.models import Client, Souscrire, Relance
from .forms import CategorieForms, GradeForms, ProduitForms, SignUpForm, LoginForm, SignupForms, SouscrireForms
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


# Create your views here.

################################################################################
#
#
#        FONCTION DE DECONNEXION
#
#
################################################################################
# @login_required(login_url='login_view')

@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return redirect('login_view')


def passwordReset_view(request):
    return render(request, 'userss/reset_password.html')


################################################################################
#
#
#                 Envoie message de confirmation par email
#
#
################################################################################


################################################################################
#
#
#                  ENREGISTREMENT D'UN UTILISATEUR
#
#
################################################################################


# @login_required(login_url='login_view')

@login_required(login_url='login_view')
def register_view(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('msgEnrg')
        else:
            msg = 'Formulaire non valide, Vérifier si vous avez choisi un mot de passe uniforme et bien sécurisé!!'

    else:
        form = SignUpForm()
    return render(request, 'accountss/register.html', {'form': form, 'msg': msg})


################################################################################
#
#
#          FONCTION DE CONNEXION POUR UTILISATEUR
#
#
################################################################################


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_role == "Administrateur":
                login(request, user)
                return redirect('home')
            elif user is not None and user.is_superuser == True:
                login(request, user)
                return redirect('home')
            elif user is not None and user.is_role == "Utilisateur":
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou Mot de passe incorrect!!")
        else:
            return redirect('login_view')
    return render(request, 'accountss/login.html',
                  {'form': form, 'login_message': 'Mot de passe ou nom d\'utilisateur incorrecte!!'})


################################################################################
#
#
#          FONCTION D'ENREGISTREMENT DU CLIENT
#
#
################################################################################



@login_required(login_url='login_view')
def client_view(request):
    submitted = False
    msg = None
    if request.method == "POST":
        form = SignupForms(request.POST, user=request.user)
        # form.fields['client'].queryset = Client.objects.filter(employe_id = request.user.pk)
        if form.is_valid():
            date_rendez_vous = form.cleaned_data['date_rendez_vous']
            delta = date_rendez_vous - date.today()
            if delta.days < 0:
                messages.warning(request, "La date de rendez-vous ne doit être antérieure à celui du jour!!")
            else:
                obj = form.save(commit=False)
                obj.employe = request.user
                obj.save()
                messages.success(request, "Client ajouté avec succes!!")
                return redirect('ajouter')
    else:
        form = SignupForms(user=request.user)
        if 'submitted' in request.Get:
            submitted = True
    context = {
        'form': form,
    }
    return render(request, 'GesClient/ajouter.html', context)


################################################################################
#
#
#            FONCTION D'ENREGISTREMENT D'UNE CATEGORIE
#
#
################################################################################


@login_required(login_url='login_view')
def categorie_view(request):
    submitted = False
    msg = None
    if request.method == "POST":
        form = CategorieForms(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employe = request.user
            obj.save()
        messages.success(request, "Categorie enregistrer avec succes!!")
        return redirect('categorie')           
    else:
        form = CategorieForms()
        if 'submitted' in request.Get:
            submitted = True
    return render(request, 'GesClient/categorie.html', {'form': form})


################################################################################
#
#
#            FONCTION D'ENREGISTREMENT D'UN GRADE
#
#
################################################################################

# @login_required(login_url='login_view')

@login_required(login_url='login_view')
def grades_view(request):
    submitted = False
    msg = None
    if request.method == "POST":
        form = GradeForms(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employe = request.user
            obj.save()
        messages.success(request, "Grade enregistrer avec succes!!")
        return redirect('grade')           
    else:
        form = GradeForms()
        if 'submitted' in request.Get:
            submitted = True
    return render(request, 'GesClient/grade.html', {'form': form})


################################################################################
#
#
#            FONCTION D'ENREGISTREMENT D'UN PRODUIT
#
#
################################################################################


@login_required(login_url='login_view')
def produit_view(request):
    submitted = False
    msg = None
    if request.method == "POST":
        form = ProduitForms(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employe = request.user
            obj.save()
        messages.success(request, "Produit enregistrer avec succes!!")
        return redirect('produit')

    else:
        form = ProduitForms()
        if 'submitted' in request.Get:
            submitted = True
    return render(request, 'GesClient/produit.html', {'form': form})


################################################################################
#
#
#               FONCTION D'ENREGISTREMENT D'UNE SOUSCRIPTION
#
#
################################################################################


@login_required(login_url='login_view')
def souscrire_view(request):
    submitted = False
    msg = None
    if request.method == "POST":
        form = SouscrireForms(request.POST)
        # form.base_field['client'].queryset = Client.objects.filter(employe_id = request.user.pk)
        if form.is_valid():
            
            date_effet= form.cleaned_data['date_effet']
            date_emission = form.cleaned_data['date_emission']
            date_echeance= form.cleaned_data['date_echeance']
            delta1 = date_effet - date.today()
            delta2 = date_echeance - date.today()
            deltaef = date_echeance - date_effet
            deltaem = date_echeance - date_emission


            # request.user
            # if delta1.days < 0 :
                                                      
            #     messages.warning(request, "La date effet ne doit être antérieure à celui du jour!!")
                
            if delta2.days < 0:
                
                messages.warning(request, "La date écheance ne doit être antérieure à celui du jour!!")
                
            elif deltaef.days < 0 :
                
                messages.warning(request, "La date effet ne doit être ultérieur à la date échéance!!")
                
            elif deltaem.days < 0:
                
                messages.warning(request, "La date emission ne doit être utltérieur à la date échéance!!")
                
            else:
                obj = form.save(commit=False) 
        
                obj.employe = request.user
                obj.save()
                messages.success(request, "Souscription enregistrer avec succes!!")
                return redirect('souscrire')
        else:
            messages.error(request, "Le formulaire n\'est pas valide !!")
            #return redirect('ErrorEnrg')
    else:
        form = SouscrireForms(user=request.user)
        if 'submitted' in request.Get:
            submitted = True
    return render(request, 'GesClient/souscrire.html', {'form': form})


################################################################################
#
#
#               FONCTION D'AFFICHAGE DE LA LISTE IMPORTE
#
#
################################################################################


@login_required(login_url='login_view')
def import_data(request):
    # datetime.datetime.now()
    now = (datetime.now().date() - timedelta(days=1))
    print(now)
    # start_date = date.now()
    # nows = start_date + (timedelta(days=365) - timedelta(days=14))
    if 'recherche' in request.GET:
        name = request.GET['recherche']
        clients = Relance.objects.filter(Q(client__icontains=name) | Q(numero_police__icontains=name))
    else:
        clients = Relance.objects.get_queryset().order_by('id')
        
    paginator = Paginator(clients, 4)  # Show 4 contacts per page
    page_list = request.GET.get('page', 4)
    page_object = paginator.get_page(page_list)
    if request.method == 'POST':
        file_format = request.POST['file-format1']
        relance_resource = RelanceResource()
        dataset = Dataset()
        new_relance = request.FILES['importData']
        if file_format == 'CSV':
            imported_data = dataset.load(new_relance.read(), format='csv')
            result = relance_resource.import_data(dataset, dry_run=True)
        elif file_format == 'XLS':
            imported_data = dataset.load(new_relance.read(), format='xls')
            # Testing data import
            result = relance_resource.import_data(dataset, dry_run=True)
        elif file_format == 'XLSX':
            imported_data = dataset.load(new_relance.read(), format='xlsx')
            # Testing data import
            result = relance_resource.import_data(dataset, dry_run=True)
        if result.has_errors():
            messages.error(request, "Une erreur s'est produite lors du lancement...")
        else:
            # Import now
            relance_resource.import_data(dataset, dry_run=False)
            messages.success(request, 'Votre fichier a été importé avec succès!')
            return redirect('import-data')

    context = {
        'client': page_object,
        'dateNow': now,
    }

    return render(request, 'GesClient/appel.html', context)







@login_required(login_url='login_view')
def import_data(request):
    now = (datetime.now().date() - timedelta(days=1))
    print(now)
    if 'recherche' in request.GET:
        name = request.GET['recherche']
        clients = Relance.objects.filter(Q(clients__icontains=name) | Q(numero_police__icontains=name))
    else:
        clients = Relance.objects.get_queryset().order_by('id')
    paginator = Paginator(clients, 4)  # Show 4 contacts per page
    page_list = request.GET.get('page', 4)
    page_object = paginator.get_page(page_list)
    if request.method == 'POST':
        file_format = request.POST['file-format1']
        relance_resource = RelanceResource()
        dataset = Dataset()
        new_relance = request.FILES['importData']

        if file_format == 'XLS':
            imported_data = dataset.load(new_relance.read(), format='xls')
            result = relance_resource.import_data(dataset, dry_run=True)
        elif file_format == 'XLSX':
            imported_data = dataset.load(new_relance.read(), format='xlsx')
            result = relance_resource.import_data(dataset, dry_run=True)

        if result.has_errors():
            messages.error(request, "Une erreur s'est produite lors du lancement...")
        else:
            relance_resource.import_data(dataset, dry_run=False)
            messages.success(request, 'Votre fichier a été importé avec succès!')
            new_relance.close()
    context = { 'client': page_object, 'dateNow': now, }
    return render(request, 'GesClient/appel.html', context)



