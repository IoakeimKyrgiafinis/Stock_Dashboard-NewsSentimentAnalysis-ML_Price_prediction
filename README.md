This python webapp which uses Flask for BackEnd and HTML/CSS for FrontEnd. 

It works the following way:
      1. Fetches stock data using EOD's Demo Api Key (STOCK SYMBOL = "MCD" ) <br/>
      2.This data is used to create a typical Stock Close Price dashboard to provide the user with
        basic historical price movement information <br/>
      3. Using the same data, an XGBRegressor is implemented in an attempt to predict tommorow's "Close"
        price using stock trade volume and historical prices
        XGBRegressor is preffered over LogisticRegression in this case because of its ability to better
        handle nonlinearity in TimeSeries which exists in this case (Financial Timeseries) <br/>
      4.At the same time feedparser is used to parse GoogleNewsRSS feed and textblob to perform sentiment
        analysis on the said feed. The result is a list of the 10 latest news and their polarity (whether 
        they are negative or positive for the stock price) <br/>


All these are then displayed on the home page of the dashboard to provide the user with some basic knowledge
about the stock. <br/>
    
The Following modules are required for this app to function:<br/>
      -flask <br/>
      -os <br/>
      -requests <br/>
      -pandas <br/>
      -dotenv <br/>
      -xgboost <br/> 
      -textblob <br/>
      -feedparser <br/>
      -EOD Demo Api Key <br/>
In order for the project to work the project path must be set like this: <br/>

FlaskStockDashboardProject/ <br/>
├── mywebapp/ <br/>
│   ├── routes/ <br/>
│   │   ├── dashboard_routes.py <br/>
│   │   └── home_routes.py <br/>
│   ├── services/ <br/>
│   │   ├── news.py <br/>
│   │   └── sentiment.py <br/>
│   ├── static/ <br/>
│   │   └── css/ <br/>
│   │       └── dashboard.css <br/>
│   ├── templates/ <br/>
│   │   ├── about.html <br/>
│   │   ├── hello.html <br/>
│   │   ├── home.html <br/>
│   │   ├── layout.html <br/>
│   │   ├── stocks_dashboard.html <br/>
│   │   └── stocks_form.html <br/>
│   ├── __init__.py <br/>
│   └── predictor.py <br/>
├── env/ <br/>
├── README.md <br/>      
          


