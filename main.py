from analyzer import SalesAnalyzer

analyzer = SalesAnalyzer("data/sales_data.csv")
analyzer.load_data()
analyzer.clean_data()

print("Gesamterlöse:", analyzer.total_revenue())
print("Durchschnittlicher Bestellwert:", analyzer.average_order_value())