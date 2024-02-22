from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from notifications.signals import notify

from .forms import BookForm
from .models import Book
 
@login_required
# Create your views here.
def bookhome(request):
    all_books = Book.objects.all()
    return render(request, 'books/home.html',{
        'title': 'Books',
        'all_books':all_books
    })
 
 
@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            sender = get_user_model().objects.get(username=request.user)
            receiver = get_user_model().objects.exclude(username=request.user)
            description = f'<b>{book.title}</b> (Book). Click <a href="/books/book-detail/{book.id}">here</a> to view.'
            notify.send(sender, recipient=receiver, verb='Upload', description=description)
            return redirect('books:home')
    else:
        form = BookForm()
    return render(request, 'books/upload_book.html',{
        'form': form,
        'title':'Upload Book'
        })
 
 
@login_required
def book_detail(request, bookid):
    current_book = Book.objects.get(pk=bookid)
    same_category_books = Book.objects.exclude(pk=current_book.id).filter(category=current_book.category)
    return render(request, 'books/book_detail.html',{
        'title':current_book.title,
        'book':current_book,
        'same_category_books': same_category_books
    })