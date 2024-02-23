from django.urls import path
from . import views
 
app_name = "books"
urlpatterns = [
    path('', views.bookhome, name='home'),
    path('upload', views.upload_book, name='upload-book'),
    path('edit/<int:bookid>', views.edit_book, name='edit-book'),
    path('book-detail/<int:bookid>', views.book_detail, name='book-detail'),
]