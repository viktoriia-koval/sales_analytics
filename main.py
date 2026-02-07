from analyzer import SalesAnalyzer
from algorithms import bubble_sort_values


def main():
    analyzer = SalesAnalyzer("data/sales_data.csv")
    analyzer.load_data()
    analyzer.clean_data()

    print("Gesamterloese:", analyzer.total_revenue())
    print("Durchschnittlicher Bestellwert:", analyzer.average_order_value())

    print("Sortieren--------------")
    analyzer.df = bubble_sort_values(analyzer.df, by="unit_price")

    analyzer.df =  analyzer.df.sort_values(by="order_amount")

    print(analyzer.df.head(20)    )


if __name__ == "__main__":
    main()
