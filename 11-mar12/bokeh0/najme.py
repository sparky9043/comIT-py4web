import requests
from bokeh.plotting import figure, show
from datetime import datetime

url = "https://query2.finance.yahoo.com/v8/finance/chart/AMD"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
data = response.json()

print(data)
timestamps = data['chart']['result'][0]['timestamp']

volumes = data['chart']['result'][0]['indicators']['quote'][0]['volume']

dates = [datetime.fromtimestamp(ts) for ts in timestamps]

time = []

for ts in timestamps:
    time.append(datetime.fromtimestamp(ts))


p = figure(x_axis_type="datetime", title="AMD Trading Volume",
           x_axis_label='Time', y_axis_label='Volume',
           width=800, height=400)



p.vbar(x=time, top=volumes, width=0.7, color="navy", alpha=0.5)

show(p)