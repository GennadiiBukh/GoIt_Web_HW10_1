from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm, AddAuthorForm

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quotes:root')  # Перенаправлення на головну сторінку після реєстрації
        return render(request, 'users/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('quotes:root')  # Перенаправлення на головну сторінку після входу
        return render(request, 'users/login.html', {'form': form})


class AddAuthorView(View):
    template_name = 'users/add_author.html'  # шлях до свого шаблону

    def get(self, request):
        form = AddAuthorForm()  # форма для додавання автора
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            # Логіка для збереження автора у базі даних
            return redirect('quotes:quote_list')  # Перенаправлення на сторінку із цитатами
        return render(request, self.template_name, {'form': form})

