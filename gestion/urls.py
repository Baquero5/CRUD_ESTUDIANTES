from django.urls import path
from . import views

urlpatterns = [
    path('', views.estudiante_list, name='estudiante_list'),
    path('estudiante/<int:pk>/', views.estudiante_detail, name='estudiante_detail'),
    path('estudiante/crear/', views.estudiante_create, name='estudiante_create'),
    path('estudiante/<int:pk>/editar/', views.estudiante_update, name='estudiante_update'),
    path('estudiante/<int:pk>/eliminar/', views.estudiante_delete, name='estudiante_delete'),
]