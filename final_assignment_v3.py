import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio
pio.renderers.default = "iframe"

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))

tesla = yf.Ticker("TSLA")

tesla_stock_data = tesla.history(period="max")

tesla_stock_data.reset_index(inplace=True)

html_data = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm")

soup = BeautifulSoup(html_data.text, 'html.parser')

tesla_data = pd.DataFrame(columns = ["Date", "Revenue"])
tag_object = soup.find_all('table')[1]

# Extract Tesla revenue data from the HTML table
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tag_object.tbody.find_all("tr"):
	cols = row.find_all("td")
	if len(cols) == 2:
		date = cols[0].text.strip()
		revenue = cols[1].text.strip()
		tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame([{"Date": date, "Revenue": revenue}])], ignore_index=True)

# Clean the Revenue column
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"",regex=True)

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail(n=5)

gamestop = yf.Ticker("GME")

gamestop_stock_data = gamestop.history(period="max")

gamestop_stock_data.reset_index(inplace=True)

html_data_2 = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html")

soup = BeautifulSoup(html_data_2.text, 'html.parser')

gme_data = pd.DataFrame(columns = ["Date", "Revenue"])
tag_object = soup.find_all('table')[1]

gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tag_object.tbody.find_all("tr"):
	cols = row.find_all("td")
	if len(cols) == 2:
		date = cols[0].text.strip()
		revenue = cols[1].text.strip()
		gme_revenue = pd.concat([gme_revenue, pd.DataFrame([{"Date": date, "Revenue": revenue}])], ignore_index=True)

# Clean the Revenue column
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"",regex=True)

gme_revenue.dropna(inplace=True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

gme_revenue.tail(n=5)

make_graph(tesla_stock_data, tesla_revenue, "Tesla")

make_graph(gamestop_stock_data, gme_revenue, "GameStop")
