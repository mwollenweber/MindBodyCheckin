from .mindbody import MindBody, loadClients, loadClasses
from django.conf import settings
from .celery import app


@app.task(name="test")
def test():
    print("This is a test")


@app.task(name="syncClients")
def syncClients():
    mbapi = MindBody()
    mbapi.authenticate(settings.SITEUSER, settings.SITEPASSWORD, settings.APIKEY, settings.SITEID)
    loadClients(mbapi)


@app.task(name="syncClasses")
def syncClasses():
    mbapi = MindBody()
    mbapi.authenticate(settings.SITEUSER, settings.SITEPASSWORD, settings.APIKEY, settings.SITEID)
    loadClasses(mbapi)
