from django.shortcuts import get_object_or_404, redirect, render
from .forms import property_form,PropertySearchForm
from django.contrib.auth.decorators import login_required
from .models import Rental
from django.contrib import messages
from django.contrib.auth import get_user_model
from notifications.signals import notify
import requests

@login_required
def rental_home(request):
    if request.method =="GET":
        form=PropertySearchForm(request.GET)
        if form.is_valid():
            search=form.cleaned_data['search']
            sort = form.cleaned_data['sort_by']
            rental_list=Rental.objects.all()
            if search:
                rental_list=rental_list.filter(address__icontains=search)
            if sort:
                if sort == 'Oldest':
                    rental_list = rental_list.order_by('-created_at')
                elif sort == 'Lowest Price':
                    rental_list = rental_list.order_by('price')
                elif sort == 'Highest Price':
                    rental_list = rental_list.order_by('-price')
                else:
                    rental_list = rental_list.order_by('created_at')

        return render(request,'rental/home.html',{'form':form,'rental_list':rental_list})
    else:
        rental_list=Rental.objects.all()
    return render(request,'rental/home.html',{
        'title': 'Rental',
        'form':form,
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
    return render(request, 'rental/upload_property.html',{'title':'Upload New Property','form':form})

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
    myAPIKey = 'c20c43b8dddc42939c4304857ea1ce69';
    url = f"https://api.geoapify.com/v1/geocode/search?text={current_rental.address} {current_rental.city} {current_rental.zip_code}&limit=1&apiKey={myAPIKey}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data["features"][0]
        latitude = result["geometry"]["coordinates"][1]
        longitude = result["geometry"]["coordinates"][0]
 
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print(f"Request failed with status code {response.status_code}")
    return render(request, 'rental/property-detail.html',{
        'title':f'Edit {current_rental.property_name}',
        'rental' : current_rental,
        'lat':latitude,
        'long': longitude
    })