from django.shortcuts import redirect

def error404(request, exception):
    # if request.user.is_authenticated:
    #     return redirect('home/')
    return redirect('welcome/')
