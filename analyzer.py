import pandas as pd
from models import EntityFactory


class SalesAnalyzer:
    def __init__(self, csv_path: str):
        # Store CSV path
        self.csv_path = csv_path
        self.df = None

    def load_data(self):
        """Load data from CSV."""
        self.df = pd.read_csv(self.csv_path)

        # Print basic structure and stats
        print("Info about the data:")
        print(self.df.info())
        print("\nStatistical summary:")
        print(self.df.describe(include="all"))

    def clean_data(self):
        """Clean data: fill missing values and remove invalid rows."""

        # Remove duplicates
        self.df.drop_duplicates(inplace=True)

        # Fill missing quantity and unit_price
        if "quantity" in self.df.columns:
            self.df["quantity"] = self.df["quantity"].fillna(0)
        if "unit_price" in self.df.columns:
            self.df["unit_price"] = self.df["unit_price"].fillna(0.0)

        # Compute missing order_amount as quantity * unit_price
        if "order_amount" in self.df.columns:
            mask = self.df["order_amount"].isna()
            self.df.loc[mask, "order_amount"] = (
                self.df.loc[mask, "quantity"] * self.df.loc[mask, "unit_price"]
            )

        # Type conversion
        self.df["order_date"] = pd.to_datetime(self.df["order_date"], errors="coerce")
        self.df["order_amount"] = pd.to_numeric(self.df["order_amount"], errors="coerce")

        # Remove invalid rows: missing date or non-positive amount
        self.df = self.df[self.df["order_date"].notna() & (self.df["order_amount"] > 0)]

        # Export cleaned data
        self.df.to_csv("data/sales_clean.csv", index=False)
        print("Cleaned data exported: data/sales_clean.csv")

    def create_objects(self):
        """Optional: create objects using EntityFactory."""
        self.products = []
        self.customers = []
        self.orders = []

        for _, row in self.df.iterrows():
            product = EntityFactory.create(
                entity_type="product",
                product_id=row["product_name"].__hash__(),
                name=row["product_name"],
                category=row["product_category"],
                base_price=row["unit_price"],
            )
            self.products.append(product)

            customer = EntityFactory.create(
                entity_type="customer",
                customer_id=row["customer_id"],
                name=row.get("customer_name", f"Customer {row['customer_id']}"),
                email=row.get("email", "unknown@example.com"),
                lifetime_value=0.0,
            )
            self.customers.append(customer)

            order = EntityFactory.create(
                entity_type="order",
                order_id=row["order_id"],
                order_date=row["order_date"],
                items=[product],
                customer=customer,
                amount=row["order_amount"],
                status=row.get("status", "completed"),
            )
            self.orders.append(order)

    def total_revenue(self):
        """Total revenue."""
        return self.df["order_amount"].sum()

    def average_order_value(self):
        """Average order value."""
        return self.df["order_amount"].mean()
