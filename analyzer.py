import pandas as pd


class SalesAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None

    def load_data(self):
        """CSV-Daten in DataFrame laden"""
        self.df = pd.read_csv(self.csv_path)

    def clean_data(self):
        """Grundlegende Datenbereinigung"""
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(inplace=True)

    def total_revenue(self):
        """Gesamterlöse"""
        return self.df["order_amount"].sum()

    def average_order_value(self):
        """Durchschnittlicher Bestellwert"""
        return self.df["order_amount"].mean()