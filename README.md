This python webapp which uses Flask for BackEnd and HTML/CSS for FrontEnd. 

It works the following way:
      1. Fetches stock data using EOD's Demo Api Key (STOCK SYMBOL = "MCD" )
      2.This data is used to create a typical Stock Close Price dashboard to provide the user with
        basic historical price movement information
      3. Using the same data, an XGBRegressor is implemented in an attempt to predict tommorow's "Close"
        price using stock trade volume and historical prices
        XGBRegressor is preffered over LogisticRegression in this case because of its ability to better
        handle nonlinearity in TimeSeries which exists in this case (Financial Timeseries)
      4.At the same time feedparser is used to parse GoogleNewsRSS feed and textblob to perform sentiment
        analysis on the said feed. The result is a list of the 10 latest news and their polarity (whether 
        they are negative or positive for the stock price)


All these are then displayed on the home page of the dashboard to provide the user with some basic knowledge
about the stock.
    
The Following modules are required for this app to function:
      -flask
      -os
      -requests
      -pandas
      -dotenv
      -xgboost
      -textblob
      -feedparser
      -EOD Demo Api Key
In order for the project to work the project path must be set like this: 

FlaskStockDashboardProject/
├── mywebapp/
│   ├── routes/
│   │   ├── dashboard_routes.py
│   │   └── home_routes.py
│   ├── services/
│   │   ├── news.py
│   │   └── sentiment.py
│   ├── static/
│   │   └── css/
│   │       └── dashboard.css
│   ├── templates/
│   │   ├── about.html
│   │   ├── hello.html
│   │   ├── home.html
│   │   ├── layout.html
│   │   ├── stocks_dashboard.html
│   │   └── stocks_form.html
│   ├── __init__.py
│   └── predictor.py
├── env/
├── README.md      
          
