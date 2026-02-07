import pandas as pd


class SalesAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.csv_path)

    def clean_data(self):
        self.df = self.df.drop_duplicates().copy()

        if "quantity" in self.df.columns:
            self.df["quantity"] = pd.to_numeric(self.df["quantity"], errors="coerce").fillna(0)
        if "unit_price" in self.df.columns:
            self.df["unit_price"] = pd.to_numeric(self.df["unit_price"], errors="coerce").fillna(0)

        if "order_amount" in self.df.columns:
            self.df["order_amount"] = pd.to_numeric(self.df["order_amount"], errors="coerce")
            missing_amount = self.df["order_amount"].isna()
            self.df.loc[missing_amount, "order_amount"] = (
                self.df.loc[missing_amount, "quantity"] * self.df.loc[missing_amount, "unit_price"]
            )

        if "order_date" in self.df.columns:
            self.df["order_date"] = pd.to_datetime(self.df["order_date"], errors="coerce")

        self.df = self.df[self.df["order_amount"].notna() & (self.df["order_amount"] > 0)]
        if "order_date" in self.df.columns:
            self.df = self.df[self.df["order_date"].notna()]

    def total_revenue(self) -> float:
        return float(self.df["order_amount"].sum())

    def average_order_value(self) -> float:
        return float(self.df["order_amount"].mean())

    def customer_count(self) -> int:
        return int(self.df["customer_id"].nunique())

    def most_profitable_category(self):
        category_revenue = (
            self.df.groupby("product_category", as_index=False)["order_amount"]
            .sum()
            .sort_values("order_amount", ascending=False)
        )
        return category_revenue.head(1)

    def top_customers_by_ltv_top10(self) -> pd.DataFrame:
        return (
            self.df.groupby("customer_id", as_index=False)["order_amount"]
            .sum()
            .rename(columns={"order_amount": "lifetime_value"})
            .sort_values("lifetime_value", ascending=False)
            .head(10)
        )

    def repeat_customer_rate(self) -> float:
        orders_per_customer = self.df.groupby("customer_id")["order_id"].nunique()
        repeat_customers = (orders_per_customer > 1).sum()
        total_customers = len(orders_per_customer)
        if total_customers == 0:
            return 0.0
        return float(repeat_customers / total_customers)

    def monthly_sales_trends(self) -> pd.DataFrame:
        work = self.df.copy()
        work["year_month"] = work["order_date"].dt.to_period("M").astype(str)
        return (
            work.groupby("year_month", as_index=False)
            .agg(revenue=("order_amount", "sum"), orders=("order_id", "nunique"))
            .sort_values("year_month")
        )

    def seasonal_sales_trends(self) -> pd.DataFrame:
        work = self.df.copy()
        work["month"] = work["order_date"].dt.month
        return (
            work.groupby("month", as_index=False)
            .agg(revenue=("order_amount", "sum"), orders=("order_id", "nunique"))
            .sort_values("month")
        )

    def average_order_size_by_category(self) -> pd.DataFrame:
        return (
            self.df.groupby("product_category", as_index=False)
            .agg(
                avg_quantity=("quantity", "mean"),
                avg_order_amount=("order_amount", "mean"),
            )
            .sort_values("avg_order_amount", ascending=False)
        )

    def status_percentages(self) -> pd.DataFrame:
        status_share = (
            self.df["status"]
            .fillna("unknown")
            .value_counts(normalize=True)
            .mul(100)
            .reset_index(name="percent") # Series -> DataFrame:
        )
        return status_share.sort_values("percent", ascending=False)

    def order_outliers(self) -> pd.DataFrame:
        q1 = self.df["order_amount"].quantile(0.25)
        q3 = self.df["order_amount"].quantile(0.75)
        
        iqr = q3 - q1 #Tukey's rule
        lower = q1 - 1.5 * iqr 
        upper = q3 + 1.5 * iqr
        
        outliers = self.df[(self.df["order_amount"] < lower) | (self.df["order_amount"] > upper)].copy()
        outliers["outlier_type"] = outliers["order_amount"].apply(
            lambda x: "small" if x < lower else "large"
        )
        return outliers.sort_values("order_amount")

    def customer_segmentation_by_spending(self) -> pd.DataFrame:
        ltv = (
            self.df.groupby("customer_id", as_index=False)["order_amount"]
            .sum()
            .rename(columns={"order_amount": "lifetime_value"})
        )

        q25 = ltv["lifetime_value"].quantile(0.25)
        q50 = ltv["lifetime_value"].quantile(0.50)
        q75 = ltv["lifetime_value"].quantile(0.75)

        bins = [float("-inf"), q25, q50, q75, float("inf")]
        labels = ["low", "mid", "high", "vip"]
        ltv["spending_tier"] = pd.cut(ltv["lifetime_value"], bins=bins, labels=labels)
        return ltv.sort_values("lifetime_value", ascending=False)

    def revenue_monthly_growth(self) -> pd.DataFrame:
        monthly = self.monthly_sales_trends().copy()
        monthly["monthly_growth_pct"] = monthly["revenue"].pct_change().mul(100)
        monthly["monthly_growth_abs"] = monthly["revenue"].diff()
        return monthly
