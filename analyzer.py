import pandas as pd
from models import EntityFactory

class SalesAnalyzer:
    def __init__(self, csv_path: str):
        # Pfad zur CSV-Datei speichern
        self.csv_path = csv_path
        self.df = None

    def load_data(self):
        """Daten aus CSV laden"""
        self.df = pd.read_csv(self.csv_path)

        # Struktur und Typen prüfen
        print("Info über die Daten:")
        print(self.df.info())
        print("\nStatistische Zusammenfassung:")
        print(self.df.describe(include='all')) # Alle Spalten einschließen

    def clean_data(self):
        """Datenbereinigung: berechnet fehlende Werte und entfernt ungültige Zeilen"""
        
        # Duplikate entfernen
        self.df.drop_duplicates(inplace=True)

        # Fehlende Werte in quantity und unit_price auffüllen
        if "quantity" in self.df.columns:
            self.df["quantity"].fillna(0, inplace=True)
        if "unit_price" in self.df.columns:
            self.df["unit_price"].fillna(0.0, inplace=True)

        # Fehlende order_amount berechnen: quantity * unit_price
        if "order_amount" in self.df.columns:
            mask = self.df["order_amount"].isna()
            self.df.loc[mask, "order_amount"] = (
                self.df.loc[mask, "quantity"] * self.df.loc[mask, "unit_price"]
            )

        # Typkonvertierung
        self.df["order_date"] = pd.to_datetime(self.df["order_date"], errors="coerce")
        self.df["order_amount"] = pd.to_numeric(self.df["order_amount"], errors="coerce")

        # Ungültige Zeilen entfernen: leere Daten oder order_amount <= 0
        self.df = self.df[self.df["order_date"].notna() & (self.df["order_amount"] > 0)]

        # Bereinigte Daten exportieren
        self.df.to_csv("data/sales_clean.csv", index=False)
        print("Bereinigte Daten exportiert: data/sales_clean.csv")

    def create_objects(self):
        """Optionale Methode: Objekte mit EntityFactory erstellen"""
        self.products = []
        self.customers = []
        self.orders = []

        for _, row in self.df.iterrows():
            # Produkt erstellen
            product = EntityFactory.create(
                entity_type="product",
                product_id=row["product_name"].__hash__(),
                name=row["product_name"],
                category=row["product_category"],
                base_price=row["unit_price"]
            )
            self.products.append(product)

            # Kunde erstellen
            customer = EntityFactory.create(
                entity_type="customer",
                customer_id=row["customer_id"],
                name=row.get("customer_name", f"Customer {row['customer_id']}"),
                email=row.get("email", "unknown@example.com"),
                lifetime_value=0.0
            )
            self.customers.append(customer)

            # Bestellung erstellen
            order = EntityFactory.create(
                entity_type="order",
                order_id=row["order_id"],
                order_date=row["order_date"],
                items=[product],
                customer=customer,
                amount=row["order_amount"],
                status=row.get("status", "completed")
            )
            self.orders.append(order)

    # -----------------------------
    # ANALYSEMETHODEN
    # -----------------------------
    def total_revenue(self):
        """Gesamterlöse"""
        return self.df["order_amount"].sum()

    def average_order_value(self):
        """Durchschnittlicher Bestellwert"""
        return self.df["order_amount"].mean()
