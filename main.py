import pandas as pd
from pycoingecko import CoinGeckoAPI
import plotly.graph_objects as go

cg = CoinGeckoAPI()

bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)
data = pd.DataFrame(bitcoin_data['prices'], columns=['TimeStamp', 'Prices'])
data['Date'] = pd.to_datetime(data['TimeStamp'], unit='ms')

candlestick_data = data.groupby(data.Date.dt.date).agg({'Prices': ['min', 'max', 'first', 'last']})

plotlyfig = go.Figure(data=[go.Candlestick(x=candlestick_data.index,
                                           open=candlestick_data['Prices']['first'],
                                           high=candlestick_data['Prices']['max'],
                                           low=candlestick_data['Prices']['min'],
                                           close=candlestick_data['Prices']['last']
                                           )
                            ])
plotlyfig.update_layout(xaxis_rangeslider_visible=False,
                        xaxis_title='Date',
                        yaxis_title='Price (USD $)',
                        title='Bitcoin Candlestick Chart over the past 30 Days')
plotlyfig.show()
