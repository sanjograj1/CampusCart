from django.shortcuts import get_object_or_404, redirect, render
from .forms import property_form
from django.contrib.auth.decorators import login_required
from .models import Rental
from django.contrib import messages

@login_required
def rental_home(request):
    rental_list=Rental.objects.all()
    return render(request,'rental/home.html',{
        'title':'Rental',
        'rental_list':rental_list
    })


@login_required
def upload_property(request):
    #if request is post
    if request.method=='POST':
        #instantiate form with post request
        form = property_form(request.POST,request.FILES)
        #validate form
        if form.is_valid():
            upload_property_var=form.save(commit=False)
            upload_property_var.seller = request.user
            upload_property_var.save()
            return redirect('rentals:home')
    else:
        form = property_form()
    return render(request, 'rental/upload_property.html',{'title':'upload New Property','form':form})

        
