from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from notifications.signals import notify
from django.contrib import messages
 
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
    current_book = get_object_or_404(Book, pk=bookid)
    same_category_books = Book.objects.exclude(pk=current_book.id).filter(category=current_book.category)
    return render(request, 'books/book_detail.html',{
        'title':current_book.title,
        'book':current_book,
        'same_category_books': same_category_books
    })
 
 
@login_required
def edit_book(request, bookid):
    my_book = get_object_or_404(Book, pk=bookid)
    if my_book.seller != request.user:
        messages.success(request, "You don't have the access to the book",extra_tags='danger')
        return redirect('accounts:user-listing')
    if request.method == 'POST':
        if 'action' in request.POST:
            form = BookForm(request.POST,request.FILES, instance=my_book)
            if form.is_valid():
                book = form.save(commit=False)
                book.save()
                return redirect('accounts:user-listing')
        else:
            my_book.delete()
            messages.success(request, "Your Book has been deleted",extra_tags='danger')
            return redirect('accounts:user-listing')
    else:    
        form = BookForm(instance=my_book)
    return render(request, 'books/edit_book.html',{
        'form': form,
        'title':'Edit Book'
        })