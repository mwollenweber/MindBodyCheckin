import traceback
from datetime import datetime, timedelta, timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.html import escape
from django.utils.timezone import make_aware
from django.template import loader
from django.conf import settings
from .models import gymClass, gymClient, gymCheckin
from .mindbody import MindBody


def validateSignIn(classid, clientid, distance, lat, long):
    # quick check for invalid input
    if classid < 1 or clientid < 1 or distance > settings.MAXDIST:
        raise ("quick invalid")

    # check if client is valid
    gClient = gymClient.objects.filter(active=True, id=clientid)
    if not gClient:
        raise ("Client is not active")

    # validate the class
    gClass = gymClass.objects.filter(active=True, id=classid)
    if not gClass:
        raise ("Class is not active")
    else:
        print("Need to check class times")

    return True


def fail(request):
    return HttpResponse("<html>Failed to sign in</html>")


def index(request):
    if request.method == 'GET':
        nw = datetime.now()
        print(f"NOW = {nw}")
        #.filter(endTime__gte=datetime.now(timezone.utc) - timedelta(minutes=20))
        g = (gymClass.objects.filter(active=True)
             #.filter(startTime__lte=datetime.now(timezone.utc) + timedelta(minutes=60))
             .filter(endTime__gte=datetime.now())
             .order_by('startTime'))

        if not g:
            g = [
                {'id': 0,
                 'name': 'No Classes',
                 'startTime': 'Available for Sign In',
                 'endTime': '',
                 'instructor': 'No Classes',
                 'location': 'No Classes',
                 'description': 'No Classes',
                 }]

        clients = gymClient.objects.filter(active=True).distinct("first_name", "last_name")
        template = loader.get_template('signin.html')
        context = {
            'title': f'{settings.GYMNAME} Sign In',
            'gymClasses': g,
            'clients': clients,
            'gymName': settings.GYMNAME,
        }
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        try:
            mbapi = MindBody()
            mbapi.authenticate(settings.SITEUSER,
                               settings.SITEPASSWORD,
                               settings.APIKEY,
                               settings.SITEID
                               )

            classid = int(request.POST.get('classid'))
            clientid = int(request.POST.get('clientid'))
            distance = float(request.POST.get('distance')) or 100.0
            lat = float(request.POST.get('lat') or 0.0)
            long = float(request.POST.get('long') or 0.0)
            print(f"classid={classid}, clientid={clientid}, distance={distance}")

            if distance > settings.MAXDIST:
                raise Exception("Unable to sign in. You're too far away!")

            if not validateSignIn(classid, clientid, distance, lat, long):
                raise Exception("Invalid Sign In")

            gymCheckin.objects.create(client_id=clientid,
                                      gymClass_id=classid,
                                      distance=distance,
                                      lat=lat,
                                      long=long,
                                      )
            mbapi.addClientToClass(clientid, classid)
            return HttpResponse("Success. You're Signed in")

        except Exception as e:
            print(traceback.format_exc())
            return HttpResponse("Error: Unable to Sign-In")


def current_datetime(request):
    now = datetime.utcnow()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def submit(request):
    return HttpResponse(escape(repr(request.POST)))
