import pandas
import datetime
import random

def add_avg_data(df: pandas.DataFrame):
    open_avg, high_avg, low_avg, close_avg, volume_avg = df["Open"].mean(),  df["High"].mean(),  df["Low"].mean(),  df["Close"].mean(),  df["Volume"].mean()

    # Флаг для того чтобы значение добавлялось каждую вторую субботу
    isItACoolDay = True

    for i in range(len(df["Date"]) - 1):
        if datetime.datetime.strptime(df["Date"][i], "%Y-%m-%d") + datetime.timedelta(days=1) != datetime.datetime.strptime(df["Date"][i + 1], "%Y-%m-%d"):
            if isItACoolDay:
                df.loc[len(df["Date"])] = [
                    datetime.datetime.strftime(datetime.datetime.strptime(df["Date"][i], "%Y-%m-%d") + datetime.timedelta(days=1), "%Y-%m-%d"), 
                    round(open_avg + (random.random() * 2 - 1)/10 * open_avg, 2), 
                    round(high_avg +(random.random() * 2 - 1)/10 * high_avg, 2), 
                    round(low_avg + (random.random() * 2 - 1)/10 * low_avg, 2), 
                    round(close_avg + (random.random() * 2 - 1)/10 * close_avg, 2), 
                    round(volume_avg + (random.random() * 2 - 1)/10 * volume_avg, 2), 
                    "USD"
                ] 
                isItACoolDay = False
            else:
                isItACoolDay = True
            # Для воскресенья 
            # df.loc[len(df["Date"])] = [
            #     datetime.datetime.strftime(datetime.datetime.strptime(df["Date"][i], "%Y-%m-%d") + datetime.timedelta(days=2), "%Y-%m-%d"), 
            #     round(open_avg + (random.random() * 2 - 1)/10 * open_avg, 2), 
            #     round(high_avg +(random.random() * 2 - 1)/10 * high_avg, 2), 
            #     round(low_avg + (random.random() * 2 - 1)/10 * low_avg, 2), 
            #     round(close_avg + (random.random() * 2 - 1)/10 * close_avg, 2), 
            #     round(volume_avg + (random.random() * 2 - 1)/10 * volume_avg, 2), 
            #     "USD"
            # ] 
            if i + 1 < len(df["Date"]) - 1:
                i = i + 1
    df.to_csv('upload/data_avg.csv', index= False)