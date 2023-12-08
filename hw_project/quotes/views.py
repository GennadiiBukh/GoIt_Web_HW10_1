from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from bson import ObjectId
from .utils import get_mongodb
from .forms import AddQuoteForm, AuthorForm, QuoteForm
from .models import Author, Tag


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


class QuoteListView(View):
    template_name = 'quotes/index.html'
    per_page = 10

    def get(self, request, page=1):
        db = get_mongodb()
        quotes = db.quotes.find()
        paginator = Paginator(list(quotes), self.per_page)
        quotes_on_page = paginator.page(page)
        return render(request, self.template_name, context={'quotes': quotes_on_page, 'paginator': paginator})


class AuthorDetailView(View):
    template_name = 'quotes/author_detail.html'

    def get(self, request, pk: str):
        db = get_mongodb()
        author = db.authors.find_one({'_id': ObjectId(pk)})
        # print(author)
        return render(request, self.template_name, context={'author': author})


class AddAuthorView(LoginRequiredMixin, View):
    login_url = "/users/login/"
    template_name = "quotes/add_author.html"

    @method_decorator(login_required)
    def get(self, request):
        form = AuthorForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = AuthorForm(request.POST)
        if form.is_valid():
            # Логіка для збереження автора у базі даних (Django та MongoDB)
            db = get_mongodb()

            # Збереження в MongoDB
            author_data = {
                'fullname': form.cleaned_data['fullname'],
                'born_date': form.cleaned_data['born_date'],
                'born_location': form.cleaned_data['born_location'],
                'description': form.cleaned_data['description'],
            }
            db.authors.insert_one(author_data)

            # Збереження в Django
            author = Author(**form.cleaned_data)
            author.save()

            return redirect('quotes:quote_list')  # Перенаправлення на сторінку із цитатами

        return render(request, self.template_name, {'form': form})


class AddQuoteView(LoginRequiredMixin, View):
    login_url = "/users/login/"
    template_name = "quotes/add_quote.html"

    @method_decorator(login_required)
    def get(self, request):
        form = QuoteForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Логіка для збереження цитати у базі даних (Django та MongoDB)
            db = get_mongodb()

            # Отримання або створення автора
            author_name = form.cleaned_data['author']
            #print(author_name.fullname, type(author_name), type(author_name.fullname))
            # author, created = Author.objects.get_or_create(fullname=author_name)  # це пошук автора в БД Django
            author = db.authors.find_one({'fullname': author_name.fullname})  # це пошук автора в БД MongoDB
            #print(author)
            # Збереження в MongoDB
            # Отримання вибраних тегів
            selected_tags = [tag.name for tag in form.cleaned_data['tags']]

            # Отримання нових тегів введених користувачем
            new_tags_input = request.POST.get('new_tags', '')
            new_tags = [tag.strip() for tag in new_tags_input.split(',') if tag.strip()]

            # Збереження нових тегів в базі даних MongoDB якщо такого тега ще немає
            for tag_name in new_tags:
                tag = db.tags.find_one({'name': tag_name})
                if not tag:
                    tag_data = {'name': tag_name}
                    db.tags.insert_one(tag_data)

            # Збереження в MongoDB
            all_tags = selected_tags + new_tags
            quote_data = {
                'quote': form.cleaned_data['quote'],
                'author': author['_id'],
                'tags': all_tags,
            }
            db.quotes.insert_one(quote_data)

            return redirect('quotes:quote_list')

        return render(request, self.template_name, {'form': form})

