import pandas as pd
from xgboost import XGBRegressor

class XGBPricePredictor:
    def __init__(self, lags=10):
        self.lags = lags
        self.model = None
        self.feature_cols = None
        self.last_date = None

    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create lag features and target column."""
        df = df.copy()
        df['target'] = df['close'].shift(-1)  # next day target
        for i in range(1, self.lags + 1):
            df[f'lag_{i}'] = df['close'].shift(i)
        df.dropna(inplace=True)
        return df

    def train(self, df: pd.DataFrame, test_ratio: float = 0.2):
        """Train the model on recent DataFrame."""
        # Ensure chronological order (oldest → newest)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        # Use only recent rows for training
        df = df.tail(250)  # last ~250 trading days
        df = self._prepare_features(df)
        self.last_date = df['date'].iloc[-1]

        # Features and target
        self.feature_cols = [c for c in df.columns if c not in ['date', 'close', 'target']]
        X = df[self.feature_cols]
        y = df['target']

        # Train/test split
        split_idx = int(len(X) * (1 - test_ratio))
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        # Train XGBoost
        self.model = XGBRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=4,
            random_state=42,
            objective='reg:squarederror'
        )
        self.model.fit(X_train, y_train)

    def predict_next_day(self, df: pd.DataFrame):
        """Predict the next day's closing price from the recent DataFrame."""
        if self.model is None or self.feature_cols is None:
            raise ValueError("Model not trained yet")

        # Ensure chronological order
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        # Use only last lags rows
        df_recent = df.tail(self.lags)
        last_row = df_recent.iloc[-1]

        # Build features for prediction
        X_pred_dict = {}
        for col in self.feature_cols:
            if col.startswith("lag_"):
                lag_num = int(col.split("_")[1])
                X_pred_dict[col] = df_recent['close'].iloc[-lag_num]
            else:
                X_pred_dict[col] = last_row[col]

        X_pred_df = pd.DataFrame([X_pred_dict])
        predicted_price = float(self.model.predict(X_pred_df)[0])  # JSON-safe

        # Compute next day date
        last_date = pd.to_datetime(last_row['date'])
        predicted_date = (last_date + pd.Timedelta(days=1)).strftime("%Y-%m-%d")

        return predicted_date, predicted_price

