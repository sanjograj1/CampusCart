def theme_processor(request):
    theme = request.COOKIES.get('theme', 'primary')
    return {'theme': theme}