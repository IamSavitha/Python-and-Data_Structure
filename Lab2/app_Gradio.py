import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gradio as gr
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

import tempfile

model = load_model('keras_model.h5')

def predict_stock(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)

    graphs = []

    # 1. Closing Price vs Time
    fig1, ax1 = plt.subplots(figsize=(10,6))
    ax1.plot(df['Close'], label='Closing Price')
    ax1.set_title(f"{ticker} Closing Price vs Time")
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend()
    graphs.append(fig1)

    # 2. Closing Price vs MA100
    ma100 = df['Close'].rolling(100).mean()
    fig2, ax2 = plt.subplots(figsize=(10,6))
    ax2.plot(df['Close'], label='Closing Price')
    ax2.plot(ma100, 'r', label='MA100')
    ax2.set_title(f"{ticker} Closing Price vs 100-Day MA")
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Price')
    ax2.legend()
    graphs.append(fig2)

    # 3. Closing Price vs MA100 and MA200
    ma200 = df['Close'].rolling(200).mean()
    fig3, ax3 = plt.subplots(figsize=(10,6))
    ax3.plot(df['Close'], label='Closing Price')
    ax3.plot(ma100, 'r', label='MA100')
    ax3.plot(ma200, 'g', label='MA200')
    ax3.set_title(f"{ticker} Closing Price vs MA100 & MA200")
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Price')
    ax3.legend()
    graphs.append(fig3)

    # ----- LSTM Prediction -----
    scaler = MinMaxScaler(feature_range=(0,1))
    data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):])
    
    data_training_array = scaler.fit_transform(data_training)
    past_100_days = data_training.tail(100)
    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
    input_data = scaler.fit_transform(final_df)

    x_test, y_test = [], []
    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100:i])
        y_test.append(input_data[i, 0])
    x_test, y_test = np.array(x_test), np.array(y_test)

    y_predicted = model.predict(x_test)
    scale_factor = 1 / scaler.scale_[0]
    y_predicted = y_predicted * scale_factor
    y_test = y_test * scale_factor

    prediction_dates = data_testing.index

    fig4, ax4 = plt.subplots(figsize=(10,6))
    ax4.plot(prediction_dates, y_test, label='Original Price', color='green')
    ax4.plot(prediction_dates, y_predicted, label='Predicted Price', color='blue')
    ax4.set_title(f"{ticker} Predicted vs Original")
    ax4.set_xlabel('Date')
    ax4.set_ylabel('Price')
    ax4.legend()
    plt.xticks(rotation=45)
    graphs.append(fig4)

    # Save Prediction Plot to a temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig4.savefig(temp_file.name)
    
    return graphs + [temp_file.name]

# Gradio UI
demo = gr.Interface(
    fn=predict_stock,
    inputs=[
        gr.Textbox(label="Enter Stock Ticker (e.g., AAPL)"),
        gr.Textbox(label="Start Date (YYYY-MM-DD)"),
        gr.Textbox(label="End Date (YYYY-MM-DD)")
    ],
    outputs=[
        gr.Plot(label="Closing Price"), 
        gr.Plot(label="Closing Price vs MA100"),
        gr.Plot(label="Closing Price vs MA100 & MA200"),
        gr.Plot(label="Predicted vs Original"),
        gr.File(label="Download Prediction Chart")
    ],
    title="📈 Stock Trend Prediction App (LSTM)",
    description="Enter stock ticker and date range to view various stock trend charts and download predictions.",
    theme="soft"  # <- makes it pretty
)

demo.launch(share=True)
