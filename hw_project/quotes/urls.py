from django.urls import path
from .views import QuoteListView, AddAuthorView, AddQuoteView
#from .views import author_detail
from .views import AuthorDetailView
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("quotes/", QuoteListView.as_view(), name='quote_list'),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name='author_detail'),
    #path("author/<int:pk>/", author_detail, name='author_detail'),
    path("add_quote/", AddQuoteView.as_view(), name='add_quote'),
    path("add_author/", AddAuthorView.as_view(), name='add_author'),
]


