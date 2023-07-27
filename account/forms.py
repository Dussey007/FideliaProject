from collections import UserList, UserString
from datetime import datetime
from http.client import HTTPResponse
# from urllib import request
from django.http import request
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import Grade, Souscrire, User, Client, Produit, Categorie, Relance
from django.forms import ModelForm
from . import models
from django.contrib.auth import get_user
from django.utils.safestring import mark_safe



profile = [
    ("Personne Morale", "Personne Morale"),
    ("Personne Physique", "Personne Physique"),
]

profileS = [
    ("*****", "*****"),
    ("PME", "Petite Moyenne Entreprise"),
    ("PMI", "Petite Moyenne Industrie"),
]

SEXES = [
    ("Masculin", "Masculin"),
    ("Feminin", "Feminin"),
    ("Societe", "Societe"),
]


class DateInput(forms.DateInput):
    input_type = 'date'




class UpperCaseInput(forms.widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        rendered_input = super().render(name, value, attrs, renderer)
        script = """
        <script type="text/javascript">
            document.getElementById('%s').addEventListener('input', function () {
                this.value = this.value.toUpperCase();
            });
        </script>
        """ % attrs['id']
        return mark_safe(rendered_input + script)





class SignupForms(ModelForm):
    nom = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control input-sm"}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    sexe = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=SEXES)
    telephone = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    adresse = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    profil = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=profile)
    profilS = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=profileS)
    date_rendez_vous = forms.DateField(required=True, widget=forms.DateInput(attrs={"class": "form-control", "type":"date"}), input_formats=['%Y-%m-%d'],) 

    class Meta:
        model = Client
        fields = (
        'nom', 'prenom', 'sexe', 'telephone', 'email', 'adresse', 'profil', 'profilS', 'date_rendez_vous', 'nomGrade',
        'employe')


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.user = kwargs.pop('user')
        super(SignupForms, self).__init__(*args, **kwargs)
        self.fields["nomGrade"].queryset = Grade.objects.all()
                # self.fields["nomGrade"].queryset = Grade.objects.filter(employe=self.user)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(SignupForms, self).save(*args, **kwargs)
        if self.request:
            obj.employe = self.request.user
        obj.save()
        return obj



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ), 
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


role = [
    ("Administrateur", "Administrateur"),
    ("Utilisateur", "Utilisateur"),
]


class ProduitForms(ModelForm):
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    nomProduit = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Produit
        fields = ('categorie', 'nomProduit', 'employe')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(ProduitForms, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(ProduitForms, self).save(*args, **kwargs)
        if self.request:
            obj.employe = self.request.user
        obj.save()
        return obj


class CategorieForms(ModelForm):
    nomCategorie = forms.CharField(max_length=40, required=True,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Categorie
        fields = ('nomCategorie', 'employe')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(CategorieForms, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(CategorieForms, self).save(*args, **kwargs)
        if self.request:
            obj.employe = self.request.user
        obj.save()
        return obj


class GradeForms(ModelForm):
    nomGrade = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    commentaires = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Grade
        fields = ('nomGrade', 'commentaires', 'employe')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(GradeForms, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(GradeForms, self).save(*args, **kwargs)
        if self.request:
            obj.employe = self.request.user
        obj.save()
        return obj

  


PROPOSES = [
    ('Réalisé', 'Réalisé'),
    ('Non réalisé', 'Non réalisé'),
    ('En attente', 'En attente'),
]


class SouscrireForms(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SouscrireForms, self).__init__(*args, **kwargs)

    souscription = forms.CharField(required=True, widget=forms.RadioSelect(choices=PROPOSES))
    prime = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "0.", }))
    date_effet = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "type":"date"}), input_formats=['%Y-%m-%d'],)
    date_echeance = forms.DateField(required=False, widget=forms.DateInput(
        attrs={"class": "form-control", "type":"date"}), input_formats=['%Y-%m-%d'],)  
    date_emission = forms.DateField(required=False, widget=forms.DateInput(
        attrs={"class": "form-control", "type":"date"}), input_formats=['%Y-%m-%d'],)
    produit = forms.ModelChoiceField(queryset=Produit.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    commentaires = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))


    class Meta:
        model = Souscrire
        fields = (
        'client', 'produit', 'souscription', 'prime', 'date_effet', 'date_echeance', 'date_emission', 'commentaires',
        'employe')

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(SouscrireForms, self).save(*args, **kwargs)
        if self.request:
            obj.employe = self.request.user
        obj.save()
        return obj


class EditProfileForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["last_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "nom...",

        }
        )

        self.fields["first_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "prénom...",

        }
        )

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "username",

        }
        )



    email = forms.EmailField(required=True,
                             widget=forms.TextInput(
                                 attrs={
                                     "class": "form-control",

                                 }
                             )
                             )

    poste = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",

            }
        )
    )


    class Meta:
        model = User
        fields = (
            'username', 'last_name', 'first_name', 'email', 'poste',
        )


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100, required=False,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, required=False,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, required=False,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class SignUpForm(UserCreationForm):
    error_message = UserCreationForm.error_messages.update({
        "duplicate_username": ("Ce nom d'utilisateur existe déjà!!"),
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["last_name"].widget.attrs.update({
            "class": "form-control",
        }
        )

        self.fields["first_name"].widget.attrs.update({
            "class": "form-control",
        }
        )
        
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
        }
        )


    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    email = forms.EmailField(required=True,
                             widget=forms.TextInput(
                                 attrs={
                                     "class": "form-control"
                                 }
                             )
                             )

    poste = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    is_role = forms.ChoiceField(required=True, choices=role)

    class Meta:
        model = User
        model._meta.get_field('email')._unique = True
        fields = ('username', 'last_name', 'first_name', 'email', 'poste', 'password1', 'password2', 'is_role')


class RelanceForms(ModelForm):
    branche = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    categorie = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    clients = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    adresse = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    numero_police = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    date_effet = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    date_expiration = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    immatriculation = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    marque = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    prime_totale = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    apporteur = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))


    class Meta:
        model = Relance
        fields = (
        'branche', 'categorie', 'clients', 'telephone', 'adresse', 'numero_police', 'date_effet', 'date_expiration',
        'immatriculation', 'marque', 'prime_totale', 'apporteur','ap1', 'ap2', 'ap3','last_modified_ap1', 'last_modified_ap2', 'last_modified_ap3')
