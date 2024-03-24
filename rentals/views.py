from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PropertyForm, PropertySearchForm
from django.contrib.auth.decorators import login_required
from .models import Rental, RentalViews
from django.contrib import messages
from django.contrib.auth import get_user_model
from notifications.signals import notify
from django.core.paginator import Paginator
import requests



@login_required
def rental_home(request):
    if request.method == "GET":
        form = PropertySearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            sort = form.cleaned_data['sort_by']
            rental_list = Rental.objects.all()
            if search:
                rental_list = rental_list.filter(address__icontains=search)
            if sort:
                if sort == 'Oldest':
                    rental_list = rental_list.order_by('-created_at')
                elif sort == 'Lowest Price':
                    rental_list = rental_list.order_by('price')
                elif sort == 'Highest Price':
                    rental_list = rental_list.order_by('-price')
                else:
                    rental_list = rental_list.order_by('created_at')

            paginator = Paginator(rental_list, 8)

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
    else:
        rental_list = Rental.objects.all()
    return render(request, 'rental/home.html', {
        'title': 'Rental',
        'form': form,
        'rental_list': rental_list,
        'page_obj':page_obj
    })


@login_required
def upload_property(request):
    # if request is post
    if request.method == 'POST':
        # instantiate form with post request
        form = PropertyForm(request.POST, request.FILES)
        # validate form
        if form.is_valid():
            upload_property_var = form.save(commit=False)
            upload_property_var.seller = request.user
            upload_property_var.save()
            sender = get_user_model().objects.get(username=request.user)
            receiver = get_user_model().objects.exclude(username=request.user)
            description = f'<b>{upload_property_var.property_name}</b> (Property). Click <a href="/rentals/property-detail/{upload_property_var.id}">here</a> to view.'
            notify.send(sender, recipient=receiver, verb='Upload', description=description)
            return redirect('rentals:home')
    else:
        form = PropertyForm()
    return render(request, 'rental/upload_property.html', {'title': 'Upload New Property', 'form': form})


@login_required
def edit_property(request, rentid):
    current_property = get_object_or_404(Rental, pk=rentid)
    if current_property.seller != request.user:
        messages.success(request, "You don't have the access to this property", extra_tags='danger')
    if request.method == 'POST':
        if 'action' in request.POST:
            form = PropertyForm(request.POST, request.FILES, instance=current_property)
            if form.is_valid():
                prop = form.save(commit=False)
                prop.save()
                return redirect('accounts:user-listing')
        else:
            current_property.delete()
            messages.success(request, "This property / rental has been deleted.", extra_tags='danger')
            return redirect('accounts:user-listing')
    else:
        form = PropertyForm(instance=current_property)
    return render(request, 'rental/edit-property.html',
                  {'form': form, 'title': f'Edit {current_property.property_name}'})


@login_required
def property_detail(request, rentid):
    current_rental = get_object_or_404(Rental, pk=rentid)
    current_viewed_properties = request.COOKIES.get('viewed_properties','')
    current_viewed_properties = [int(book) for book in current_viewed_properties.split(',') if book]
    if rentid not in current_viewed_properties:
        current_viewed_properties.append(rentid)

    current_viewed_properties_str = ','.join(map(str, current_viewed_properties)) 
    response = HttpResponse("Viewed Properties")    
    myAPIKey = 'c20c43b8dddc42939c4304857ea1ce69'
    url = f"https://api.geoapify.com/v1/geocode/search?text={current_rental.address} {current_rental.city} {current_rental.zip_code}&limit=1&apiKey={myAPIKey}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["features"]:
            result = data["features"][0]
            userlatitude = result["geometry"]["coordinates"][1]
            userlongitude = result["geometry"]["coordinates"][0]
        else:
            userlatitude = 42.31749
            userlongitude = -83.0387979

    else:
        userlatitude = 42.31749
        userlongitude = -83.0387979

    urldistance = f"https://api.geoapify.com/v1/routematrix?apiKey={myAPIKey}"
    headers = {"Content-Type": "application/json"}
    if userlongitude and userlongitude:
        source_location = [userlongitude, userlatitude]
        data = f'{{"mode":"bus","sources":[{{"location":{source_location}}}],"targets":[{{"location":[-83.0387979, 42.31749]}},{{"location":[-83.06649144027972, 42.305201350000004]}}]}}'
        try:
            resp = requests.post(urldistance, headers=headers, data=data)
            json_resp = resp.json()
            distance_values = [item['distance'] for sublist in json_resp['sources_to_targets'] for item in sublist]
        except requests.exceptions.HTTPError as e:
            print(e.response.text)
            
    free_view = RentalViews.objects.filter(user_session_key=request.session.session_key, rental=current_rental)
    if not free_view.exists():
        RentalViews.objects.create(rental=current_rental, user=request.user, user_session_key=request.session.session_key)            
    response = render(request, 'rental/property-detail.html', {
        'title': f'Edit {current_rental.property_name}',
        'rental': current_rental,
        'lat': userlatitude,
        'long': userlongitude,
        'maincampuslat': 42.305201350000004,
        'maincampuslong': -83.06649144027972,
        'maccampuslat': 42.31749,
        'maccampuslong': -83.0387979,
        'distance_values': distance_values,
        'maincampusdistance': distance_values[1],
        'maccampusdistance': distance_values[0]
    })
    response.set_cookie('viewed_properties', current_viewed_properties_str, max_age=36000)
    return response
