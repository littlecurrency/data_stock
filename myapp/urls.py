from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_data, name='submit_data'),
    path('view-content/', views.view_content, name='view_content'),
    path('modify/', views.modify, name='modify'),
    path('edit_company/', views.edit_company, name='edit_company'),
    path('update_company/', views.update_company, name='update_company'),

]
