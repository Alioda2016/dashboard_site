from django.urls import path

from . import views

urlpatterns = [
    path('', views.source_list, name='source_list'),
    # path('process-selected/', views.process_selected, name='process_selected'),
    path('output-graph/', views.process_selected, name='output_graph'),
    path('output-graph/relevant/', views.process_relevant_source, name='process_relevant'),
    path('output-graph/relevant_selected/', views.process_relevant_selected, name='selected_results'),
    path('output-graph/categorical_relevant/', views.categorical_relevant_source, name='categorical_relevant'),
]
