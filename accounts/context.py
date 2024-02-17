def profile_image(request):
    profile_image = request.user.profile.profile_image
    return {'profile_image': profile_image}