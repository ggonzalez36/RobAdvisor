from robadv.models import Company, UserProfile
from django.contrib.auth.models import User
user=User.objects.create(id=1, username="carl")
userProfile = UserProfile(userid=user)
userProfile.save()
users1= User.objects.all()
users= UserProfile.objects.all().delete()


user=User.objects.all()
userProfile=UserProfile.objects.all()
for x in user :
    userProfile = UserProfile(userid=x)
    userProfile.save()


userObj=User.objects.get(username="kostolom")
userProfile=UserProfile(userID=userObj)
for x in userProfile :
      print(x. user, x.age, x.initialInvestment,x.timeInvest,x.risklevel)


a = Company(name="Google", abreviation="GOOG")
a.save()
a = Company(name="IBM", abreviation="IBM")
a.save()
a = Company(name="Apple", abreviation="APP")
a.save()
a = Company(name="Amazon", abreviation="AMZN")
a.save()
##################################################

from robadv.models import Company,Stock, Prediction
from RoboAdvisor1.stocker import Stocker
from RoboAdvisor1.PredictStock import predict_future
PredictionList=predict_future(6)






stockOrder = stock.stock.iloc[::-1]
x = 300
for index, row in stockOrder.iterrows():

    if x >=0:
        DateFixed=row['Date']
        StringDate=str(DateFixed)
        print(StringDate[0:10], row['Close'], row['Volume'])
        persistingStock = Stock(companyFK=company, dateStock=StringDate[0:10], close=row['Close'], volume=row['Volume'])
        persistingStock.save()
        x-=1

companies= Company.objects.all()
for x in companies :
    b=Prediction(company=x, day=30, nshares=100)
    b.save()
    print(x.id)


#########################################################
from robadv.models import UserProfile, UserProjection, Portfolio,Transaction
from datetime import  date, timedelta
userProfile=UserProfile.objects.all()
for x in userProfile :
      print(x.pk, x.user, x.age, x.initialInvestment,x.timeInvest,x.risklevel)



userProfile=UserProfile.objects.get(pk=1);
print(userProfile)
today = date.today()
months=userProfile.timeInvest*12;
i = userProfile.initialInvestment
for month in range(months):
    time = timedelta(days=month*30)

    timetotal= today +time
    #userProjection = UserProjection(userid=userProfile, date=timetotal, investment=i)
    #userProjection.save()
    print(month,month*30, time,i , timetotal)
    i = i + i * 0.15

UserProfile.objects.all().delete()
userProjection=UserProjection.objects.all().delete()
portfolio=Portfolio.objects.all().delete()
for x in userProjection:
    print(x.date, x.investment, x.userid)



portfolio=Portfolio( assetClass='UK Stocks', tarjet=35, marketValue=userProfile.initialInvestment*0.35)
portfolio.save()

################
from robadv.models import Transaction
transaction=Transaction.objects.all().delete()
for x in transaction:
    print(transaction)



UserProfile.objects.all().delete()
userProjection=UserProjection.objects.all().delete()
portfolio=Portfolio.objects.all().delete()

########################################
from robadv.models import UserProfile, UserProjection, Portfolio

portfolio=Portfolio.objects.all()

for x in portfolio:
    print( x.userid, x.assetId, x.assetClass, x.marketValue, x.returned)

############################
from robadv.models import Company
bp=Company.objects.get(pk=10)
bp.shares=0
bp.save()







from robadv.models import Company
from robadv.Persist.Persist import CreateStock, UpdateCompany
companies=Company.objects.all()
for x in companies:
        print(x.pk, x.abreviation)
        UpdateCompany(x.abreviation)



from robadv.models import Company, Prediction, PredictionList, Portfolio , UserProfile

userProfile=UserProfile(userid=userObj)
print(int(userProfile.initialInvestment))


from robadv.Persist.Persist import UpdateCompany, UpdateStock, BuyShares , RebalancePortfolio, CreateProjection, DailyUpdate, CreateCompany
from robadv.models import Company, Prediction, PredictionList, Portfolio , UserProfile, Performance, Stock
from django.contrib.auth.models import User





users=User.objects.all()
userObj=User.objects.get(username="we32")
userProfile=UserProfile(userid=userObj)
CreateCompany(3)
companies=Company.objects.filter(category=3 )
for company in companies:
   UpdateStock(company, 360)





company=Company.objects.get(abreviation='AMEA.F')
UpdateStock(company, 360)
#CreateProjection(companies ,userProfile)

#DailyUpdate(userProfile, companies)



from robadv.Persist.Persist import UpdateCompany, UpdateStock, BuyShares , RebalancePortfolio, CreateProjection, DailyUpdate, CreateCompany
from robadv.models import Company, Prediction, PredictionList, Portfolio , UserProfile, Performance, Stock
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

userObj=User.objects.get(username="dairus")
userProfile=UserProfile(userid=userObj)
last=userProfile.lastUpdate-timedelta(10)
today=date.today()
companies=Company.objects.all()


for x in range((today - last).days):
    print(x)
    invest = 0;
    for company in companies:
        if company.shares != 0:
            #stock=Stock.objects.get(dateStock=today-timedelta(x),companyFK=company.id)
            #invest = invest + stock.close * company.shares

            print( company.price, today-timedelta(x))



    performance = Performance.objects.create(userid=userProfile, date=today-timedelta(x),amount=round(invest, 2))
    performance.save()
    userProfile.initialInvestment = round(invest, 2)
    userProfile.save()



from robadv.Persist.Persist import UpdateCompany, UpdateStock, BuyShares , RebalancePortfolio, CreateProjection, DailyUpdate, CreateCompany
from robadv.models import Company, Prediction, PredictionList, Portfolio , UserProfile, Performance, Stock
companies=Company.objects.all()
for company in companies:
    UpdateStock(company , 0)


