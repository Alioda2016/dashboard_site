from django.urls import path

from . import views

urlpatterns = [
    path('', views.source_list, name='source_list'),
    # path('process-selected/', views.process_selected, name='process_selected'),
    path('output-graph/', views.process_selected, name='output_graph'),
]
