import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df[['close']]
    df.rename(columns={'close': 'Close'}, inplace=True)
    return df

def plot_historical_data(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Close'], label='Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Historical Price Data')
    plt.legend()
    plt.savefig('static/historical_data.png')

def predict_prices(df, periods=30):
    model = ExponentialSmoothing(df['Close'], trend='add', seasonal='add', seasonal_periods=365)
    model_fit = model.fit()
    forecast = model_fit.forecast(periods)

    forecast_df = pd.DataFrame(forecast, columns=['Predicted'])
    forecast_df.index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=periods)
    forecast_df.to_csv(f'static/prediction_{periods}.csv')

    plt.figure(figsize=(10, 5))
    plt.plot(df['Close'], label='Closing Price')
    plt.plot(forecast_df['Predicted'], label='Predicted Price', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'Price Prediction for {periods} Days')
    plt.legend()
    plt.savefig(f'static/prediction_{periods}.png')

    return forecast_df.iloc[-1]['Predicted']

# Load data
data = load_data('data/ethereum_price.csv')

# Initial prediction plots
for years in range(1, 6):
    predict_prices(data, periods=years * 365)
