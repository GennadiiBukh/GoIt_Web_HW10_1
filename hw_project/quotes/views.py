from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .utils import get_mongodb
from .forms import AddQuoteForm, AuthorForm, QuoteForm
from .models import Author

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


# def author_detail(request, pk):
#     author = get_object_or_404(Author, pk=pk)
#     return render(request, 'quotes/author_detail.html', {'author': author})

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

    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        return render(request, self.template_name, context={'author': author})


class AddAuthorView(CreateView):
    template_name = "quotes/add_author.html"
    form_class = AuthorForm
    success_url = reverse_lazy("quotes:quote_list")

class AddQuoteView(CreateView):
    template_name = "quotes/add_quote.html"
    form_class = QuoteForm
    success_url = reverse_lazy("quotes:quote_list")

    def get(self, request):
        form = AddQuoteForm()  # форма для додавання цитат
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            # Логіка для збереження цитати у базі даних
            return redirect('quotes:quote_list')  # Перенаправлення на сторінку із цитатами
        return render(request, self.template_name, {'form': form})


