import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
import streamlit as st 
from sklearn.preprocessing import MinMaxScaler

st.title('Stock Trend Prediction Analysis')

user_input = st.text_input('Enter Stock Ticker Symbol', 'AAPL')
start = '2020-01-01'
end = '2025-12-31'
df = yf.download(user_input, start, end)

st.subheader(f'Data from Yahoo Finance {start[0:4]} - {end[0:4]}')
st.write(df.describe())
#df.columns = df.columns.droplevel(1)

st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize=(10,6))
plt.plot(df['Close'])
st.pyplot(fig)


st.subheader('Closing Price vs Time chart (MA 100)')
MA100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(10,6))
plt.plot(df['Close'])
plt.plot(MA100, 'r')
st.pyplot(fig)


st.subheader('Closing Price vs Time chart (MA 100 and 200)')
MA100 = df.Close.rolling(100).mean()
MA200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(10,6))
plt.plot(df['Close'])
plt.plot(MA100, color='red', label='MA 100')
plt.plot(MA200, color='green', label='MA 200')
st.pyplot(fig)


#splitting data into training and testing sets

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing =  pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])
print(data_training.shape)
print(data_testing.shape)


scalar = MinMaxScaler(feature_range=(0,1))


data_training_array = scalar.fit_transform(data_training)

#Load ML Model 
model = load_model('keras_model.h5')


past_100_days = data_training.tail(100)


final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scalar.fit_transform(final_df)


x_test = []
y_test = []

for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])

x_test, y_test = np.array(x_test), np.array(y_test)

y_predicted = model.predict(x_test)

scaler = scalar.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

#Final graph 
st.subheader('Prediction Vs Original')
fig2 = plt.figure(figsize=(10,6))
plt.plot(y_test,'y',label ='Original Price')
plt.plot(y_predicted,'r',label ='Predicted Price')

plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)