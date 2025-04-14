import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gradio as gr
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load model only once
model = load_model('keras_model.h5')

def predict_stock(ticker):
    start = '2020-01-01'
    end = '2025-12-31'
    
    df = yf.download(ticker, start=start, end=end)

    # Preprocess and visualize
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

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(y_test, label='Original Price', color='yellow')
    ax.plot(y_predicted, label='Predicted Price', color='red')
    ax.set_title(f"Prediction vs Original for {ticker}")
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.legend()

    return fig

# Gradio UI
demo = gr.Interface(
    fn=predict_stock,
    inputs=gr.Textbox(label="Enter Stock Ticker (e.g., AAPL)"),
    outputs=gr.Plot(label="Prediction vs Original"),
    title="📈 Stock Trend Prediction (LSTM)",
    description="Enter a stock ticker to see the predicted vs actual closing price trend.",
)

demo.launch(share=True)
