from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('logins/', views.login_view, name='login_view'),
    path('quiter/', views.logout_view, name='quiter'),
    path('registers/', views.register_view, name='log'),
    path('client/', views.client_view, name='client'),
    path('ajoutGrade/', views.grades_view, name='gradeAj'),
    path('categorieA/', views.categorie_view, name='categ'),
    path('produitA/', views.produit_view, name='prod'),
    path('souscrires/', views.souscrire_view, name='souscription'),
    path('import-data/', views.import_data, name="import_data"),
    
    path('password_reset/', PasswordResetView.as_view(  template_name = 'userss/reset_password.html'  ), name='password_reset'),
    
    path('password_reset/done/', PasswordResetDoneView.as_view(    template_name = 'userss/password_reset_done.html' ), name = 'password_reset_done' ),
    
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(    template_name = 'userss/password_reset_confirm.html' ), name='password_reset_confirm'),
    
    path('password_reset/complete/', PasswordResetCompleteView.as_view(  template_name = 'userss/password_reset_complete.html'), name = 'password_reset_complete')
    
    
    
]