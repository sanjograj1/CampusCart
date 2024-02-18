def profile_image(request):
    if request.user.is_authenticated:
        profile_image = request.user.profile.profile_image
    else:
        profile_image = 'default.png'
    return {'profile_image': profile_image}