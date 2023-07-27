from django.forms import fields, Field, widgets
from import_export import resources
from import_export.fields import Field
from django.core.exceptions import ObjectDoesNotExist
from account.models import Relance
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from import_export.results import RowResult






class RelanceResource(resources.ModelResource):
    instances_to_keep = set()

    branche = Field(saves_null_values=False, column_name='Branche', attribute='branche')
    categorie = Field(saves_null_values=False, column_name='Catégorie', attribute='categorie')
    clients = Field(saves_null_values=False, column_name='Client', attribute='clients')
    telephone = Field(saves_null_values=False, column_name='Téléphone', attribute='telephone')
    adresse = Field(saves_null_values=False, column_name='Adresse', attribute='adresse')
    numero_police = Field(saves_null_values=False, column_name='Numero Police', attribute='numero_police')
    date_effet = Field(saves_null_values=False, column_name='Date Effet', attribute='date_effet')
    date_expiration = Field(saves_null_values=False, column_name='Date Expiration', attribute='date_expiration')
    immatriculation = Field(saves_null_values=False, column_name='Immatriculation', attribute='immatriculation')
    marque = Field(saves_null_values=False, column_name='Marque', attribute='marque')
    prime_totale = Field(saves_null_values=False, column_name='Prime Totale', attribute='prime_totale')
    apporteur = Field(saves_null_values=False, column_name='Apporteur', attribute='apporteur')

    class Meta:
        model = Relance
        exclude = ['id']
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('branche', 'categorie', 'clients', 'telephone', 'adresse', 'numero_police', 'date_effet', 'date_expiration', 'immatriculation', 'marque', 'prime_totale', 'apporteur')

    def after_save_instance(self, instance, using_transactions, dry_run):
        self.instances_to_keep.add(instance.id)
        
    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        Relance.objects.exclude(id__in=self.instances_to_keep).delete()
        
        
    # def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
    #     for row in dataset:
    #         instance_loader = self._meta.model.objects.get_loader_for_update(
    #             row, self.get_fields(), self.get_instance_kwargs(row))
    #         try:
    #             instance = instance_loader.get_instance()
    #         except ObjectDoesNotExist:
    #             instance = None

    #         if instance:
    #             # update existing instance
    #             self.import_obj(instance, row, dry_run)
    #         else:
    #             # create new instance
    #             self.import_obj(None, row, dry_run)

    #     # delete any instances not included in the import
    #     self.instances_to_keep.update(self._meta.model.objects.filter(**self.get_filters()).values_list('id', flat=True))
    #     self._meta.model.objects.exclude(id__in=self.instances_to_keep).delete()
    
    
    
    
    
    
    
    
    
    


        


    # def imports_data(self, dataset, dry_run=False, raise_errors=False, use_transactions=None, collect_failed_rows=False, **kwargs):
    #         # Ajouter le code de vérification ici
    #         existing_immatriculations = set(Relance.objects.values_list('immatriculation', flat=True))
    #         rows = dataset.dict
    #         for row in rows:
    #             immatriculation = row['Immatriculation']
    #             if immatriculation in existing_immatriculations:
    #                 # L'élément existe déjà dans la table immatriculation
    #                 row_result = RowResult()
    #                 row_result.import_type = RowResult.IMPORT_TYPE_SKIP
    #                 row_result.errors.append(ValidationError(f"L'immatriculation {immatriculation} existe déjà dans la base de données."))
    #                 row_result.message.warning("L'immatriculation {immatriculation} existe déjà dans la base de données.")
    #                 if collect_failed_rows:
    #                     row_result.diff = row
    #                     self.append_failed_row(row_result)
    #                 continue
    #             existing_immatriculations.add(immatriculation)

    #             # Importer l'élément
    #             resultats = super().import_data([row], dry_run, raise_errors, use_transactions, collect_failed_rows, **kwargs)
    #             self.after_import(dataset, resultats, using_transactions=True, dry_run=dry_run)
            
    #         return resultats