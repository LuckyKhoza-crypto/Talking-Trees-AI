from django.urls import path, include
from . import views
import django_cas_ng.views
# import admin

urlpatterns = [
    path("", views.home, name="home"),
    path('advancedSearchResult', views.advancedSearch,
         name='advancedSearchResult'),
    path('randomSearchResult', views.randomSearchResult,
         name='randomSearchResult'),
    path('post_comment/<str:tree_id>', views.post_comment, name='post_comment'),

    path('accounts/login', django_cas_ng.views.LoginView.as_view(),
         name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(),
         name='cas_ng_logout'),

    path('upload', views.import_Data.as_view(), name='upload'),

    path('chat/', views.chat_view, name='chat_view'),
    path('response', views.display_chatbot_response, name='response')
]
