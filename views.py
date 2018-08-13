from django.http import Http404
from django.shortcuts import render, get_object_or_404,render_to_response
from .models import Company, Stock,Prediction, PredictionList, UserProfile, UserProjection, Portfolio,Transaction,Performance
from chartit import DataPool, Chart
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm, SetPrediction,UserProfileForm, deposit  ,transfer
from django.contrib import messages
from RoboAdvisor1.stocker import Stocker
from datetime import  date, datetime, timedelta
from django.contrib.auth.models import User
from robadv.Persist.Persist import UpdateCompany, UpdateStock, BuyShares , RebalancePortfolio, CreateProjection, DailyUpdate, CreateCompany, buyshare
from RoboAdvisor1.PredictStock import predict_future
from celery.schedules import crontab
from celery.task import periodic_task


@periodic_task(run_every=crontab())
def every_month(userProfile):
    print("Asset Day" )
    #userProfile.lastUpdate=date.today()



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                try:

                    login(request, user)
                    albums = UserProfile.objects.filter(userid=request.user)
                    userProfile = get_object_or_404(UserProfile, userid=request.user)
                    context = {'userProfile': userProfile, 'albums': albums}
                    return render(request, 'roboadvisor/Profile.html', context)

                except:

                    return render(request, 'roboadvisor/welcome.html')
    context = {
        "form": form,
    }
    return render(request, 'roboadvisor/register.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'roboadvisor/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            try:
                print(request.user)
                userProfile =UserProfile.objects.get(userid=request.user)

                cht = generalGraph(request, userProfile.pk)
                print("exists USER")
                context = {'userProfile': userProfile,'weatherchart': cht }
                return render(request, 'roboadvisor/Profile.html', context)

            except UserProfile.DoesNotExist:
                return render(request, 'roboadvisor/welcome.html')
            else:
                return render(request, 'roboadvisor/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'roboadvisor/login.html', {'error_message': 'Invalid login'})
    return render(request, 'roboadvisor/login.html')


def stockDetails(request, assetId):
    userProfile = UserProfile.objects.get(userid=request.user)
    portfolio = Portfolio.objects.get(assetId=assetId, userid=userProfile.pk)
    companies= Company.objects.filter(category=assetId)
    today=date.today()

    if not (today.weekday() == 5) | (today.weekday() == 6):
        for company in companies:
            if (company.lastUpdate<today ) :
                UpdateCompany(company)
                #UpdateStock(company, 0)
    if(userProfile.accountAge % 30 == 0):

        if (RebalancePortfolio( userProfile,userProfile.accountAge/30 )):
            messages.success(request, 'Portfolio rebalanced ' + str(userProfile.userid))

        else:
            messages.warning(request, 'Portafolio rebalanced according a bad performance')

    context = {'assetId':assetId, 'portfolio':portfolio, 'companies':companies,'today':today }
    return render(request, 'roboadvisor/stockDetails.html', context)

def welcome(request):
    userObj = User.objects.get(username=request.user)
    print(userObj.id, userObj.username)
    userProfile = UserProfile.objects.create(userid=userObj)

    form = UserProfileForm(request.POST or None, instance=userProfile)
    if form.is_valid():
        userProfile = form.save(commit=False)
        userProfile.userid = request.user
        userProfile.age = request.POST["age"]
        userProfile.initialInvestment = request.POST["initialInvestment"]
        userProfile.initialInvestment=int(userProfile.initialInvestment)
        userProfile.timeInvest = request.POST["timeInvest"]
        userProfile.risklevel = request.POST["risklevel"]
        userProfile.creationDate = date.today() -timedelta(28)
        userProfile.lastUpdate = date.today() -timedelta(28)
        userProfile.save()
        messages.success(request, 'Risk Profile Store ' + str(userProfile.userid))
    else:
        userProfile.delete()
        print("unvalid form")
        return render(request, 'roboadvisor/welcome.html')
    companies = Company.objects.all()
    totalInvested=BuyShares(companies, userProfile)
    print(userProfile.initialInvestment, totalInvested)
    userProfile.initialInvestment = totalInvested
    userProfile.save()
    performance = Performance(userid=userProfile, date=date.today(), amount=totalInvested)
    performance.save()
    userProjection = CreateProjection(companies, userProfile)
    portfolio = updatePortfolio(userProfile.userid)
    invest = performance.amount

    cht = generalGraph(request, userProfile.pk)
    context = {'userProfile': userProfile, 'form': form, 'weatherchart': cht, 'userProjection': userProjection,
                 'invest': invest, 'totalinvested': totalInvested
         , 'portfolio': portfolio}
    return render(request, 'roboadvisor/Profile.html', context)

def profile(request):
    userProfile=UserProfile.objects.get(userid=request.user)
    every_month(userProfile)
    portfolio = Portfolio.objects.filter(userid=userProfile.pk)
    userProjection = UserProjection.objects.filter(userid=userProfile.pk).last()
    cht=generalGraph(request,userProfile.pk)

    form = deposit(request.POST or None)
    today = date.today()
    companies=Company.objects.all()
    invest=userProfile.initialInvestment
    if(userProfile.lastUpdate<today):
        DailyUpdate(userProfile, companies)


    if form.is_valid():

        if request.method == 'POST' and 'Deposit' in request.POST:
            transaction = form.save(commit=False)
            transaction.amount = request.POST["amount"]
            transaction = Transaction(userid=userProfile, date=datetime.now(), type=1, amount=int(transaction.amount) )
            transaction.save()
            performance = Performance(userid=userProfile, date=datetime.now())
            userProfile.initialInvestment = userProfile.initialInvestment +  int(transaction.amount)
            userProfile.save()
            buyshare(int(transaction.amount), userProfile)
            performance.amount = invest +  int(transaction.amount)
            performance.save()
            messages.success(request, 'Deposit successful ' + str(transaction.amount))
        elif request.method == 'POST' and 'Transfer' in request.POST:
            transaction = form.save(commit=False)
            transaction.amount = request.POST["amount"]
            transaction = Transaction(userid=userProfile, date=datetime.now(), type=2, amount=int(transaction.amount))
            transaction.save()
            performance = Performance(userid=userProfile, date=datetime.now())
            userProfile.initialInvestment = userProfile.initialInvestment - int( transaction.amount)
            userProfile.save()
            performance.amount = invest -  int(transaction.amount)
            performance.save()
            messages.success(request, 'Transfer successful ' + str(transaction.amount))


    else:
        print("unvalid form in Profile")
        context = {'userProfile': userProfile,'today':today,'invest':invest,
                   'weatherchart': cht,
                   'userProjection': userProjection,
                   'portfolio': portfolio}
        return render(request, 'roboadvisor/Profile.html', context)


    #portfolio = updatePortfolio(userProfile.userid)
    cht = generalGraph(request, userProfile.pk)
    context = {'userProfile': userProfile,'today':today, 'invest':invest,
               'weatherchart': cht,
               'userProjection': userProjection,
               'portfolio': portfolio}
    return render(request, 'roboadvisor/Profile.html', context)



def generalGraph (request, userId):
# Step 1: Create a DataPool with the data we want to retrieve.
    Stockdata = \
        DataPool(
            series=
            [{'options': {
                'source': UserProjection.objects.filter(userid=userId)
            },
                'terms': [
                    'date',
                    'investment']}
            ])
    cht = Chart(
                datasource = Stockdata,
                series_options =
                  [{'options':{
                      'type': 'area',
                      'stacking': False},
                    'terms':{
                        'date':['investment']
                      }}],
                chart_options =
                  {'title': {
                       'text': 'Estimate return  '},
                   'xAxis': {
                        'title': {
                           'text': 'Day'}}})
    return cht






def updatePortfolio(userid):
    userProfile = UserProfile.objects.get(pk=userid)
    Portfolio.objects.filter(userid=userProfile.pk).delete()
    if (userProfile.risklevel == 3):
        portfolio = Portfolio(userid=userProfile,assetId=1, assetClass='UK Stocks', tarjet=35,
                              marketValue=userProfile.initialInvestment * 0.35)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=2, assetClass='Foreign Stocks', tarjet=31,
                              marketValue=userProfile.initialInvestment * 0.31)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=3, assetClass='Emerging Markets', tarjet=20,
                              marketValue=userProfile.initialInvestment * 0.20)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=4,assetClass='Dividend Stocks', tarjet=10,
                              marketValue=userProfile.initialInvestment * 0.1)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=5,assetClass='Municipal Bonds', tarjet=4,
                              marketValue=userProfile.initialInvestment * 0.04)
        portfolio.save()
    elif (userProfile.risklevel == 2):
        portfolio = Portfolio(userid=userProfile,assetId=1, assetClass='UK Stocks', tarjet=35,
                              marketValue=userProfile.initialInvestment * 0.35)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=2, assetClass='Foreign Stocks', tarjet=24,
                              marketValue=userProfile.initialInvestment * 0.24)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=3, assetClass='Emerging Markets', tarjet=16,
                              marketValue=userProfile.initialInvestment * 0.16)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=4, assetClass='Dividend Stocks', tarjet=8,
                              marketValue=userProfile.initialInvestment * 0.08)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=5, assetClass='Municipal Bonds', tarjet=17,
                              marketValue=userProfile.initialInvestment * 0.17)
        portfolio.save()
    else:
        portfolio = Portfolio(userid=userProfile,assetId=1, assetClass='UK Stocks', tarjet=35,
                              marketValue=userProfile.initialInvestment * 0.26)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=2, assetClass='Foreign Stocks', tarjet=31,
                              marketValue=userProfile.initialInvestment * 0.17)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=3, assetClass='Emerging Markets', tarjet=20,
                              marketValue=userProfile.initialInvestment * 0.11)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=4, assetClass='Dividend Stocks', tarjet=10,
                              marketValue=userProfile.initialInvestment * 0.11)
        portfolio.save()
        portfolio = Portfolio(userid=userProfile,assetId=5, assetClass='Municipal Bonds', tarjet=4,
                              marketValue=userProfile.initialInvestment * 0.35)
        portfolio.save()
    portfolio = Portfolio.objects.filter(userid=userProfile.pk)
    return portfolio



def index(request):
    CompanyList = Company.objects.all()
    context= {'CompanyList': CompanyList}
    return render(request, 'roboadvisor/index.html',context)

def graph(request,company_id ):
# Step 1: Create a DataPool with the data we want to retrieve.
    Stockdata = \
        DataPool(
            series=
            [{'options': {
                'source': Stock.objects.filter(companyFK=company_id)},
                'terms': [
                    'dateStock',
                    'close']},
            {'options': {
                'source': PredictionList.objects.filter(predictionFK=company_id)},
                'terms': [

                    {'dateStock_2':'dateStock', 'prediction':'estimate'}]}
            ])
    cht = Chart(
                datasource = Stockdata,
                series_options =
                  [{'options':{
                      'type': 'line',
                      'stacking': False},
                    'terms':{
                        'dateStock':['close']
                      }},
                    {'options':{
                      'type': 'line',
                      'stacking': False},
                    'terms':{
                        'dateStock_2':['prediction']
                      }}
                  ],
                chart_options =
                  {'title': {
                       'text': 'Performance last Year'},
                   'xAxis': {
                        'title': {
                           'text': 'Month number'}}})
    return cht

def detail(request, company_id):

    try:
        cht=graph(request,company_id)
        company= Company.objects.get(pk=company_id)
        stockslist=Stock.objects.filter(companyFK=company_id)
        predictionlink = "http://127.0.0.1:8000/robadv/" + company_id + "/prediction"
        graphPredicted = "http://127.0.0.1:8000/robadv/" + company_id + "/predicted"
        graph3=  "http://127.0.0.1:8000/robadv/" + company_id + "/compare"
        context = {'Company': company,
                   'StockList': stockslist,
                   'weatherchart': cht,
                   'predictionlink':predictionlink,
                   'graphPredicted':graphPredicted,
                   'graph3':graph3}
    except Company.DoesNotExist:
        raise Http404("Company does not exist")
    return render(request, 'roboadvisor/detail.html', context)


def createPrediction(request, company_id):


    stockslist = Stock.objects.filter(companyFK=company_id)
    predictionlink = "http://127.0.0.1:8000/robadv/" + company_id + "/prediction"
    graphPredicted = "http://127.0.0.1:8000/robadv/" + company_id + "/predicted"
    graph3 = "http://127.0.0.1:8000/robadv/" + company_id + "/compare"
    prediction = get_object_or_404(Prediction, company=company_id)
    company = get_object_or_404(Company, pk=company_id)
    form = SetPrediction(request.POST or None, instance=prediction)

    if form.is_valid():
        for predictionElement in PredictionList.objects.filter(predictionFK=company_id):
            predictionElement.delete()
        prediction= form.save(commit=False)
        prediction.company=company
        prediction.day=prediction.day
        prediction.save()
        predict_future(company_id, prediction.day)
        messages.success(request, 'Prediction days updated to '+ str(prediction.day) )
        cht = graph(request, company_id)

        context = {

            'prediction':prediction,
            'weatherchart': cht,
            'StockList': stockslist,
            'Company': company,
            'predictionlink':predictionlink,
            'graphPredicted': graphPredicted,
            'graph3': graph3

        }
        return render(request, 'roboadvisor/detail.html', context)

    else:

        context = {
        "form": form,
        }
    return render(request, 'roboadvisor/prediction.html', context)


def graphPrediction(request, company_id):
    # Step 1: Create a DataPool with the data we want to retrieve.
    Stockdata = \
        DataPool(
            series=
            [{'options': {
                'source': PredictionList.objects.filter(predictionFK=company_id)},
                'terms': [
                    'dateStock',
                    'estimate']}
            ])
    cht = Chart(
        datasource=Stockdata,
        series_options=
        [{'options': {
            'type': 'line',
            'stacking': False},
            'terms': {
                'dateStock': ['estimate']
            }}],
        chart_options=
        {'title': {
            'text': 'Predicted Values'},
            'xAxis': {
                'title': {
                    'text': 'Month number'}}})
    return render_to_response('roboadvisor/graph.html', {'weatherchart': cht})


def account(request):

    userProfile = UserProfile.objects.get(userid=request.user)
    transactions=Transaction.objects.filter(userid=userProfile.pk).order_by('-date')
    cht = graphHistory( userProfile.pk)
    context= {'weatherchart': cht, 'transactions':transactions, }
    return render(request, 'roboadvisor/account.html', context)

def graphHistory( userId):

    Stockdata = \
        DataPool(
            series=
            [{'options': {
                'source': Performance.objects.filter(userid=userId)
            },
                'terms': [
                    'date',
                    'amount']}
            ])
    cht = Chart(
        datasource=Stockdata,
        series_options=
        [{'options': {
            'type': 'area',
            'stacking': False},
            'terms': {
                'date': ['amount']
            }}],
        chart_options=
        {'title': {
            'text': 'Historical performance  '},
            'xAxis': {
                'title': {
                    'text': 'Day'}}})
    return cht
