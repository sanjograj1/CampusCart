from django.shortcuts import get_object_or_404, redirect, render
from .forms import property_form
from django.contrib.auth.decorators import login_required
from .models import Rental
from django.contrib import messages
from django.contrib.auth import get_user_model
from notifications.signals import notify

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
            sender = get_user_model().objects.get(username=request.user)
            receiver = get_user_model().objects.exclude(username=request.user)
            description = f'<b>{upload_property_var.property_name}</b> (Property). Click <a href="/rentals/property-detail/{upload_property_var.id}">here</a> to view.'
            notify.send(sender, recipient=receiver, verb='Upload', description=description)
            return redirect('rentals:home')
    else:
        form = property_form()
    return render(request, 'rental/upload_property.html',{'title':'upload New Property','form':form})

@login_required
def edit_property(request,rentid):
    current_property=get_object_or_404(Rental,pk=rentid)
    if current_property.seller != request.user:
        messages.success(request, "You don't have the access to this property", extra_tags='danger')
    if request.method=='POST':
        if 'action' in request.POST:
            form=property_form(request.POST,request.FILES,instance=current_property)
            if form.is_valid():
                prop=form.save(commit=False)
                prop.save()
                return redirect('accounts:user-listing')
        else:
            current_property.delete()
            messages.success(request, "This property / rental has been deleted.", extra_tags='danger')
            return redirect('accounts:user-listing')
    else:
        form=property_form(instance=current_property)
    return render(request,'rental/edit-property.html',{'form':form,'title':f'Edit {current_property.property_name}'})

        
@login_required
def property_detail(request, rentid):
    current_rental = get_object_or_404(Rental, pk=rentid)
    rental_list=Rental.objects.all()
    # get same city rentals
    same_city_rentals = Rental.objects.exclude(pk=current_rental.id).filter(city=current_rental.city)
 
    return render(request, 'rental/property-detail.html',{'title':f'{current_rental.property_name} details','same_city_rentals':same_city_rentals, 'rental' : current_rental})