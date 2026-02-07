from datetime import date


# Basisklasse für alle Entitäten
class Entity:
    def __init__(self, entity_id: int):
        if not isinstance(entity_id, int):
            raise ValueError("Die ID muss eine ganze Zahl sein")
        self.id = entity_id

    def __str__(self):
        return f"Entity(id={self.id})"

    def __repr__(self):
        return self.__str__()


# Product
class Product(Entity):
    def __init__(self, product_id: int, name: str, category: str, base_price: float):
        super().__init__(product_id)

        if base_price < 0:
            raise ValueError("Der Basispreis muss sein >= 0")

        self.name = name
        self.category = category
        self.base_price = float(base_price)

    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.base_price})"

    def __repr__(self):
        return self.__str__()


# Customer
class Customer(Entity):
    def __init__(self, customer_id: int, name: str, email: str, lifetime_value: float = 0.0):
        super().__init__(customer_id)

        if lifetime_value < 0:
            raise ValueError("lifetime_value muss sein >= 0")

        self.name = name
        self.email = email
        self.lifetime_value = float(lifetime_value)

    def __str__(self):
        return f"Customer(id={self.id}, name={self.name}, LTV={self.lifetime_value})"

    def __repr__(self):
        return self.__str__()


# Order
class Order(Entity):
    def __init__(self, order_id: int, order_date: date, items: list,
                 customer: Customer, amount: float, status: str):
        super().__init__(order_id)

        if amount < 0:
            raise ValueError("Der Betrag muss >= 0")

        self.order_date = order_date
        self.items = items
        self.customer = customer
        self.amount = float(amount)
        self.status = status

    def __str__(self):
        return f"Order(id={self.id}, amount={self.amount}, status={self.status})"

    def __repr__(self):
        return self.__str__()


# Factory pattern
class EntityFactory:
    @staticmethod
    def create(entity_type: str, **kwargs):
        if entity_type == "product":
            return Product(**kwargs)
        elif entity_type == "customer":
            return Customer(**kwargs)
        elif entity_type == "order":
            return Order(**kwargs)
        else:
            raise ValueError("Unbekannter Entitätstyp")
