from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import Permission, User
from datetime import date

# the following lines added:
import datetime
from django.utils import timezone

class UserProfile(models.Model):
    userid =models.OneToOneField(
            User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    age= models.IntegerField(default=18)
    initialInvestment= models.BigIntegerField(default=0)
    timeInvest= models.IntegerField(default=0)
    risklevel=models.IntegerField(default=0)
    creationDate = models.DateField(auto_now_add=False, default=date.today)
    lastUpdate = models.DateField(auto_now_add=False, default=date.today)
    accountAge=models.IntegerField(default=1)


class Performance(models.Model):
    userid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    amount=models.FloatField(default=0)




class UserProjection(models.Model):
    userid= models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False, blank=True)
    investment=models.IntegerField(default=18)
    nmonth = models.IntegerField(default=0)

class Portfolio(models.Model):
    userid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    assetId=models.IntegerField(default=0)
    assetClass=models.CharField(max_length=200)
    tarjet=models.IntegerField(default=0)
    marketValue=models.IntegerField(default=0)
    returned=models.FloatField(default=0)
    description=models.CharField(max_length=1000)





class Company(models.Model):
    name = models.CharField(max_length=50)
    abreviation = models.CharField(max_length=10, default="GOOG")
    category=models.IntegerField(default=0)
    price=models.FloatField(default=0)
    change=models.FloatField(default=0)
    shares=models.FloatField(default=0)
    lastUpdate = models.DateField(auto_now_add=False, default=date.today)


class Transaction(models.Model):
    userid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    companyFK= models.ForeignKey(Company, on_delete=models.CASCADE,  blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True, blank=True)
    type=models.IntegerField(default=0)
    amount= models.IntegerField(default=0)


class Stock(models.Model):
        companyFK = models.ForeignKey(Company, on_delete=models.CASCADE)
        dateStock = models.CharField(max_length=10)
        close = models.FloatField(default=1)
        volume = models.IntegerField(default=1)

class Prediction(models.Model):
        company  = models.OneToOneField(
            Company,
        on_delete=models.CASCADE,
        primary_key=True,
    )
        day= models.IntegerField(default=0)
        nshares=models.IntegerField(default=0)



class PredictionList(models.Model):
    predictionFK = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    dateStock = models.CharField(max_length=10)
    estimate=models.FloatField(default=0)
    change=models.FloatField(default=0)