from datetime import datetime, timezone

from django.template.backends import django
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


SEXES = [
    ("Masculin", "Masculin"),
    ("Feminin", "Feminin"),
    ("Societe", "Societe"),
]

profile = [
    ("Personne Morale", "Personne Morale"),
    ("Personne Physique", "Personne Physique"),
]

profileS = [
    ("*****", "*****"),
    ("PME", "Petite Moyenne Entreprise"),
    ("PMI", "Petite Moyenne Industrie"),
]

ROLES = [
    ("Administrateur", "Administrateur"),
    ("Utilisateur", "Utilisateur"),
]


class User(AbstractUser):
    is_role = models.CharField(max_length=20, choices=ROLES, blank=True)
    poste = models.CharField(max_length=30)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # self.username = self.username.upper()
        self.last_name = self.last_name.upper()
        self.first_name = self.first_name.title()
        self.poste = self.poste.title()
        if self.is_role == "Administrateur":
            self.is_superuser = True
        super(User, self).save(*args, **kwargs)


class Grade(models.Model):
    employe = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, null=True)
    nomGrade = models.CharField(max_length=40, unique=True)
    commentaires = models.TextField(max_length=150)

    def __str__(self):
        return self.nomGrade
    
    def save(self, *args, **kwargs):
        self.nomGrade = self.nomGrade.upper()
        super(Grade, self).save(*args, **kwargs)


class Client(models.Model):
    employe = models.ForeignKey(User, blank=True, on_delete=models.PROTECT, null=True)
    nom = models.CharField(max_length=40, verbose_name="nom", null=False)
    prenom = models.CharField(max_length=40, verbose_name="prenom")
    sexe = models.CharField(max_length=40, choices=SEXES, verbose_name="genre")
    telephone = models.IntegerField(verbose_name="telephone")
    email = models.EmailField(verbose_name="email", unique=True)
    adresse = models.CharField(max_length=40, verbose_name="adresse")
    profil = models.CharField(max_length=20, choices=profile, verbose_name="profil")
    profilS = models.CharField(max_length=20, choices=profileS, verbose_name="profil societe",
                               blank=True)  
    nomGrade = models.ForeignKey(Grade, blank=True, on_delete=models.PROTECT, null=True)
    date_rendez_vous = models.DateField(blank=False, verbose_name="date rendez vous")

    def __str__(self):
        return f'{self.nom} {self.prenom}'
    
    def save(self, *args, **kwargs):
        self.nom = self.nom.upper()
        self.prenom = self.prenom.title()
        self.profil = self.profil.title()
        super(Client, self).save(*args, **kwargs)



class Relance(models.Model):
    branche = models.CharField(max_length=200, default="vide")
    categorie = models.CharField(max_length=200, default="vide")
    clients = models.CharField(max_length=200, default="vide")
    telephone = models.CharField(max_length=100, default="vide")
    adresse = models.CharField(max_length=70, default="vide")
    numero_police = models.CharField(max_length=30, default="vide")
    date_effet = models.DateField(max_length=20, default="vide")
    date_expiration = models.DateField(max_length=20, default="vide")
    immatriculation = models.CharField(max_length=150, default="vide")
    marque = models.CharField(max_length=60, default="vide")
    prime_totale = models.BigIntegerField(default="vide")
    apporteur = models.CharField(max_length=50, default="vide")
    ap1 = models.BooleanField(default=False)
    ap2 = models.BooleanField(default=False)
    ap3 = models.BooleanField(default=False)
    last_modified_ap1 = models.DateTimeField(null=True, blank=True)
    last_modified_ap2 = models.DateTimeField(null=True, blank=True)
    last_modified_ap3 = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.branche

    def save(self, *args, **kwargs):
        if self.ap1 == True and self.last_modified_ap1 is None :
            self.last_modified_ap1 = datetime.now()
        elif self.ap2 == True and self.last_modified_ap2 is None:
            self.last_modified_ap2 = datetime.now()
        elif self.ap3 ==True and self.last_modified_ap3 is None: 
            self.last_modified_ap3 = datetime.now()
        super(Relance, self).save(*args, **kwargs)

    class Meta:
        db_table = "account_relance"



class Categorie(models.Model):
    employe = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, null=True)
    nomCategorie = models.CharField(max_length=40, unique=True, blank=True)

    def __str__(self):
        return self.nomCategorie
    
    
    def save(self, *args, **kwargs):
        self.nomCategorie = self.nomCategorie.upper()
        super(Categorie, self).save(*args, **kwargs)


class Produit(models.Model):
    employe = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, null=True, verbose_name="categorie")
    nomProduit = models.CharField(max_length=40, unique=True, verbose_name="nom produit")

    def __str__(self):
        return self.nomProduit


class Souscrire(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, null=True)
    employe = models.ForeignKey(User, blank=True, on_delete=models.PROTECT, null=True)
    client = models.ForeignKey(Client, blank=True, on_delete=models.PROTECT, verbose_name="client")
    souscription = models.CharField(max_length=40, verbose_name="proposition")
    prime = models.CharField(max_length=40, verbose_name="primes", default="0")
    date_effet = models.DateField(blank=True, null=True, verbose_name="date effet")
    date_echeance = models.DateField(blank=True, null=True, verbose_name="date echeance")
    date_emission = models.DateField(blank=True, null=True, verbose_name="date emission")
    commentaires = models.TextField(max_length=150, default="aucun commentaires")

    def __str__(self):
        return self.client

    @property
    def confirm_or_not(self):
        return "confirmé" if self.souscription else "non confirmé"

    @property
    def vide_or_not(self):
        if self.date_effet is None:
            return "Aucune"
        else:
            return self.date_effet

    @property
    def videE_or_not(self):
        if self.date_emission is None:
            return "Aucune"
        else:
            return self.date_effet

    @property
    def vides_or_not(self):
        if self.date_echeance is None:
            return "Aucune"
        else:
            return self.date_echeance
