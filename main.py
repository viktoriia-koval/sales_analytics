from time import perf_counter

from analyzer import SalesAnalyzer
from algorithms import linear_search_numeric, bubble_sort_values


def main():
    analyzer = SalesAnalyzer("data/sales_data.csv")
    analyzer.load_data()
    analyzer.clean_data()

    print("Gesamterloese:", analyzer.total_revenue())
    print("Durchschnittlicher Bestellwert:", analyzer.average_order_value())

    print("Sortieren--------------")

    bubble_input = analyzer.df.copy()
    t1 = perf_counter()
    bubble_sorted = bubble_sort_values(bubble_input, by="unit_price")
    bubble_time = perf_counter() - t1

    pandas_input = analyzer.df.copy()
    t2 = perf_counter()
    pandas_sorted = pandas_input.sort_values(by="order_amount")
    pandas_time = perf_counter() - t2

    print(f"bubble_sort_values time: {bubble_time:.6f} s")
    print(f"pandas sort_values time: {pandas_time:.6f} s")
    if pandas_time > 0:
        print(f"Speed ratio (bubble/pandas): {bubble_time / pandas_time:.2f}x")

    print("Search--------------")
    targ = 2

    t1 = perf_counter()
    found_rows_loop = linear_search_numeric(analyzer.df, field="quantity", target=targ)
    loop_time = perf_counter() - t1

    t2 = perf_counter()
    found_rows_loc = analyzer.df.loc[analyzer.df["quantity"] == targ]
    loc_time = perf_counter() - t2

    print(f"Linear search target quantity={targ}")
    print(f"Found rows (loop): {len(found_rows_loop)}")
    print(f"Found rows (loc): {len(found_rows_loc)}")
    print(f"loop search time: {loop_time:.6f} s")
    print(f"loc search time: {loc_time:.6f} s")
    if loc_time > 0:
        print(f"Speed ratio (loop/loc): {loop_time / loc_time:.2f}x")

    #print(bubble_sorted.head(20))
    #print(pandas_sorted.head(20))


if __name__ == "__main__":
    main()
