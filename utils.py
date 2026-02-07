from pathlib import Path

import matplotlib.pyplot as plt

from analyzer import SalesAnalyzer


def create_visualizations(analyzer: SalesAnalyzer):
    output_dir = Path("output/figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1) Bar chart: revenue by category
    category_revenue = (
        analyzer.df.groupby("product_category", as_index=False)["order_amount"]
        .sum()        
    )

    plt.figure(figsize=(8, 5))
    plt.bar(category_revenue["product_category"], category_revenue["order_amount"])
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_dir / "revenue_by_category.png", dpi=150)
    plt.close()

    # 2) Line chart: monthly revenue trend
    monthly = analyzer.monthly_sales_trends()
    plt.figure(figsize=(9, 5))
    plt.plot(monthly["year_month"], monthly["revenue"], marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "monthly_revenue_trend.png", dpi=150)
    plt.close()

    # 3) Histogram: order value distribution
    plt.figure(figsize=(8, 5))
    plt.hist(analyzer.df["order_amount"], bins=40, edgecolor="black")
    plt.title("Order Value Distribution")
    plt.xlabel("Order Amount")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(output_dir / "order_value_distribution.png", dpi=150)
    plt.close()
