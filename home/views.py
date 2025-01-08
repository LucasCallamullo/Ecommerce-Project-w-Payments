from django.shortcuts import render

# Create your views here.
def home(request):
    
    context = {
        "1": 1
    }
    
    return render(request, "home/home.html", context)