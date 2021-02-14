from django.http import HttpResponse


# Create your views here.
def welcome(request):
    return HttpResponse(request.session['Starling'])
