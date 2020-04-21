from django.urls import path
from . import views
from mysite import settings
from django.conf.urls.static import static
urlpatterns = [
    #Home Page
    path('', views.show_home_page, name = 'home'),
    path('check_progress_query_sample/', views.check_progress_query_sample, name = 'check_progress_query_sample'),
    path('run_refgen/', views.run_refgen, name = 'run_refgen'),
    #Sample Query Page
    path('show_sample_query_result/', views.show_sample_query_result_page, name = 'show_sample_query_result_page'),
    path('show_sample_query_result/table/', views.show_sample_query_result_table, name = 'show_query_result_table'),
    path('update_sample_selection/', views.update_sample_selection, name = 'update_sample_selection'),
    #Refgen selection page
    path('show_refgen_query_result/', views.show_refgen_query_result_page, name = 'show_refgen_query_result_page'),
    path('show_refgen_query_result/table/', views.show_refgen_query_result_table, name = 'show_refgen_query_result_table'),
    path('check_progress_download_feature_table/', views.check_progress_download_feature_table, name = 'check_progress_download_feature_table'),
    #Feature table
    path('show_feature_table/', views.show_feature_table_page, name = 'show_feature_table_page'),
    path('show_feature_table/table/', views.show_feature_table, name = 'show_feature_table'),
    path('check_progress_submit_job/', views.check_progress_submit_job, name = 'check_progress_submit_job'),
    #Submitted
    path('submitted',views.show_submitted_page, name = 'show_submitted_page'),
]
'''
path('query/submit/', views.query_metadata, name = 'submit_query'),
path('query/show/', views.show_query_result_page, name = 'show_query_page'),
path('query/show/table/', views.show_query_result, name = 'show_query_table'),
path('query/show_refgen/',views.show_refgen_result_page, name = 'show_refgen_page'),
path('query/show_refgen/table/', views.show_refgen_result, name = 'show_refgen_table'),
path('query/query_feature_table/',views.query_feature_table_download, name = 'query_feature_table_download'),
path('query/show_feature_table_result/', views.show_feature_table_result_page, name = 'show_feature_table_result_page'),
path('query/show_feature_table_result/table/', views.show_feature_table_result, name = 'show_feature_table_result'),

path('submitted',views.show_submitted_page, name = 'show_submitted_page'),
'''
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
