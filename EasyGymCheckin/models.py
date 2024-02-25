from django.db import models


class gymClass(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    startTime = models.DateTimeField(blank=True, editable=True)
    endTime = models.DateTimeField(blank=True, editable=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.id


class gymClient(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    email = models.CharField(max_length=200, blank=True, null=True)
    homePhone = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    photoURL = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.id


class gymCheckin(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(gymClient, on_delete=models.CASCADE)
    gymClass = models.ForeignKey(gymClass, on_delete=models.CASCADE)
    checkinTime = models.DateTimeField(auto_now=True, editable=True)
    lat = models.FloatField(blank=True, editable=True, default=0)
    long = models.FloatField(blank=True, editable=True, default=0)
    distance = models.FloatField(blank=True, editable=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return self.id
