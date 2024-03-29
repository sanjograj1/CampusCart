from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from notifications.signals import notify
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import BookForm,BooksFilter
from .models import Book, BookViews


@login_required
# Create your views here.
def bookhome(request):
    if request.method == 'GET':
        form = BooksFilter(request.GET)
        if form.is_valid():
            book_name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            price_range = form.cleaned_data['price']
            books = Book.objects.all()
            if category:
                books = books.filter(category=category)
            if price_range:
                price = price_range.split('-')
                books = books.filter(price__gte=price[0], price__lte=price[1])
            if book_name:
                books = books.filter(title__contains=book_name)

            paginator = Paginator(books, 9)

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
    else:
        books = Book.objects.all()
    return render(request, 'books/home.html', {
        'title': 'Books',
        'all_books': books,
        'form': form,
        'page_obj':page_obj
    })


@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
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
    return render(request, 'books/upload_book.html', {
        'form': form,
        'title': 'Upload Book'
    })


@login_required
def book_detail(request, bookid):
    current_book = get_object_or_404(Book, pk=bookid)

    # get same category books
    same_category_books = Book.objects.exclude(pk=current_book.id).filter(category=current_book.category)

    # Update viewed_books in the cookies
    current_viewed_books = request.COOKIES.get('viewed_books', '')
    current_viewed_books = [int(book) for book in current_viewed_books.split(',') if book]
    if bookid not in current_viewed_books:
        current_viewed_books.append(bookid)

    current_viewed_books_str = ','.join(map(str, current_viewed_books))
    book_view = BookViews.objects.filter(user_session_key=request.session.session_key,book=current_book)
    if not book_view.exists():
        BookViews.objects.create(book=current_book, user=request.user, user_session_key=request.session.session_key)

    response = render(request, 'books/book_detail.html', {
        'title': current_book.title,
        'book': current_book,
        'same_category_books': same_category_books
    })
    response.set_cookie('viewed_books', current_viewed_books_str, max_age=36000)
    return response


@login_required
def edit_book(request, bookid):
    my_book = get_object_or_404(Book, pk=bookid)
    if my_book.seller != request.user:
        messages.success(request, "You don't have the access to the book", extra_tags='danger')
        return redirect('accounts:user-listing')
    if request.method == 'POST':
        if 'action' in request.POST:
            form = BookForm(request.POST, request.FILES, instance=my_book)
            if form.is_valid():
                book = form.save(commit=False)
                book.save()
                return redirect('accounts:user-listing')
        else:
            my_book.delete()
            messages.success(request, "Your Book has been deleted", extra_tags='danger')
            return redirect('accounts:user-listing')
    else:
        form = BookForm(instance=my_book)
    return render(request, 'books/edit_book.html', {
        'form': form,
        'title': 'Edit Book'
    })
