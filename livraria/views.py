from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddBookForm
from .models import Book

def home(request):
    books = Book.objects.all()
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['senha']            
        user = authenticate(
            request,
            username = username,
            password = password
        )
        if user is not None:
            login(request, user)
            messages.success(request,'Login bem sucedido')  
            return redirect('home')
        else:
            messages.error(request,'Erro na autenticação')
            return redirect('home')
    else:
        return render(request, 'home.html', {'books': books})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(
        request,
        'Logout realizado com sucesso'
    )
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Você fez login com sucesso com novo usuário")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def book_detail(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        return render(request, 'book.html', {'book': book})
    else:
        messages.error('Nao foi possivel ver os detalhes de um livro')
        return redirect('home')


def book_delete(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        book.delete()
        messages.success(request, 'Parabens deletou um livro')
        return redirect('home')
    else:
        messages.error(request, 'Erro precisa estar autenticado')
        return redirect('home')

def book_add(request):
    form = AddBookForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Tudo deu certo')
                return redirect('home')
        return render(request, 'add_book.html', {'form': form})
    else:
        messages.error(request, 'deu erro tente de novo')
        return redirect('home')

def book_update(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        form = AddBookForm(request.POST or None, instance= book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atualização bem sucedida')
            return redirect('home')
        return render(request, 'update_book.html', {'form': form})
    else:
        messages.error(request, 'Erro tente novamente')
        return redirect('home')

def livros(request):
    return HttpResponse('mama eu')