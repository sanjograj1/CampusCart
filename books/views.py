from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import BookForm
from .models import Book
 
@login_required()
# Create your views here.
def bookhome(request):
    all_books = Book.objects.all()
    return render(request, 'books/home.html',{
        'title': 'Books',
        'all_books':all_books
    })
 
 
@login_required()
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('books:home')
    else:
        form = BookForm()
    return render(request, 'books/upload_book.html',{'form': form})
 
 
@login_required
def book_detail(request, bookid):
    current_book = Book.objects.get(pk=bookid)
    return render(request, 'books/book_detail.html',{
        'title':current_book.title,
        'book':current_book
    })