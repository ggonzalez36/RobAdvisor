import pandas as pd
import fbprophet
from datetime import date, datetime

from robadv.models import Company,Stock, Prediction, PredictionList


def create_model():
        # Make the model
    model = fbprophet.Prophet(daily_seasonality='auto',
                                  weekly_seasonality='auto',
                                  yearly_seasonality='auto',
                                  changepoint_prior_scale=0.05,
                                  changepoints=None)


    # Add monthly seasonality
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)

    return model


def remove_weekends( dataframe):

        # Reset index to use ix
        dataframe = dataframe.reset_index(drop=True)

        weekends = []

        # Find all of the weekends
        for i, date in enumerate(dataframe['ds']):
            if (date.weekday() == 5) | (date.weekday() == 6):
                weekends.append(i)

        # Drop the weekends
        dataframe = dataframe.drop(weekends, axis=0)

        return dataframe





def predict_future( company_id, days):
    prediction = Prediction.objects.get( company=company_id)
    stockslist = Stock.objects.filter(companyFK=company_id)
    i = 0
    df = pd.DataFrame(columns=['ds', 'y'])
    for stock in stockslist:

        dateF = datetime.strptime(stock.dateStock, '%Y-%m-%d')
        #print(dateF, stock.close)
        df.loc[i] = [dateF, stock.close]
        i += 1;

    model = create_model()
    model.fit(df)

    future = model.make_future_dataframe(periods=days, freq='D')
    future = model.predict(future)
    future = future[future['ds'] >= datetime.today()]
    future = remove_weekends(future)
    future = future.dropna()

    for index, row in future.iterrows():
        StringDate = str(row['ds'])
        print(row['ds'], row['yhat'])
        predictionList = PredictionList(predictionFK=prediction, dateStock=StringDate[0:10], estimate=row['yhat'])
        predictionList.save()







