from django.shortcuts import render , HttpResponse
from django.http import HttpResponse

# Create your views here.
###def home(request):
###    return HttpResponse("Welcome!!!!") # בכדי להחזיר טקסט חוזר מהבקשת  HTTPS
###    #return render(request, "home.html")  #בכדי לדבר עם הHTML
###
#def register(request):
#    return render(request, 'users/register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # כאן תוכל להוסיף לוגיקה לשמירת הנתונים במסד נתונים
        return HttpResponse(f"משתמש {username} נרשם בהצלחה!")
    return render(request, 'users/register.html')