import json
import sys

class InvalidIdException(Exception):
    pass

class InvalidPriceException(Exception):
    pass

class Entity:
    def __init__(self, id, name, city, address):
        if id < 0:
            raise InvalidIdException("Invalid id")
        self.id = id
        self.name = name
        self.city = city
        self.address = address

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id}, name='{self.name}', city='{self.city}', address='{self.address}')"

class Customer(Entity):
    """
    Represents a customer in the Matamazon system.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Customer name.
        - city (str): Customer city.
        - address (str): Customer shipping address.

    Exceptions:
        InvalidIdException: If 'id' is not valid according to the specification.

    Printing:
        Must support printing in the following format (example):
            Customer(id=42, name='Daniel Elgarici', city='Karmiel, address='123 Main Street')
        Exact formatting requirements appear in the assignment PDF.
    """

    # TODO implement this class as instructed
    pass



class Supplier(Entity):
    """
    Represents a supplier in the Matamazon system.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Supplier name.
        - city (str): Warehouse city (origin city for shipping).
        - address (str): Warehouse address.

    Exceptions:
        InvalidIdException: If 'id' is not valid according to the specification.

    Printing:
        Must support printing in the following format (example):
            Supplier(id=42, name='Yinon Goldshtein', city='Haifa, address='32 David Rose Street')
    """

    # TODO implement this class as instructed
    pass


class Product:
    """
    Represents a product sold on the Matamazon website.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier.
        - name (str): Product name.
        - price (float): Non-negative price.
        - supplier_id (int): ID of the supplier that provides the product.
        - quantity (int): Non-negative quantity in stock.

    Exceptions:
        InvalidIdException:
            - If id/supplier_id is invalid per specification.
        InvalidPriceException:
            - If price is invalid (e.g., negative).

    Printing:
        Must support printing in the following format (example):
            Product(id=101, name='Harry Potter Cushion', price=29.99, supplier_id=42, quantity=555)
    """

    # TODO implement this class as instructed
    def __init__(self, id, name, price, supplier_id, quantity):
        if id < 0 or supplier_id < 0:
            raise InvalidIdException("Invalid id")
        if price < 0:
            raise InvalidPriceException("Invalid price")
        self.id = id
        self.name = name
        self.price = price
        self.supplier_id = supplier_id
        self.quantity = quantity

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, supplier_id={self.supplier_id}, quantity={self.quantity})"

    def __lt__(self, other):
        return self.price < other.price

class Order:
    """
    Represents a placed order.

    Required fields (per specification):
        - id (int): Unique non-negative integer identifier (assigned by the system).
        - customer_id (int): ID of the customer who placed the order.
        - product_id (int): ID of the ordered product.
        - quantity (int): Ordered quantity (non-negative integer).
        - total_price (float): Total price for the order (non-negative).

    Exceptions:
        InvalidIdException:
            - If one of the ID fields is invalid.
        InvalidPriceException:
            - If total_price is invalid.

    Printing:
        Must support printing in the following format (example):
            Order(id=1, customer_id=42, product_id=101, quantity=10, total_price=299.9)

    """

    # TODO implement this class as instructed
    def __init__(self, id, customer_id, product_id, quantity, total_price):
        if id < 0 or customer_id < 0 or product_id < 0:
            raise InvalidIdException("Invalid id")
        if total_price < 0:
            raise InvalidPriceException("Invalid price")
        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

    def __repr__(self):
        return f'Order(id={self.id}, customer_id={self.customer_id}, product_id={self.product_id}, quantity={self.quantity}, total_price={self.total_price})'


class MatamazonSystem:
    """
    Main system class that stores and manages customers, suppliers, products and orders.

    The system must support:u
        - Registering customers/suppliers (with unique IDs across both types).
        - Adding/updating prodcts (must validate supplier existence).
        - Placing orders (validate product existence and stock).
        - Removing objects by ID and type (with dependency constraints).
        - Searching products by name/query and optional max price.
        - Exporting system state to a text file (customers/suppliers/products only).
        - Exporting orders to JSON grouped by supplier origin city.

    Notes:
        - The specification does not require specific internal fields. Any data structures are allowed,
          as long as the behaviors match the spec.
        - A parameterless constructor is required.
    """

    def __init__(self):
        """
        Initialize an empty Matamazon system.

        Requirements:
            - Must be parameterless.
            - Internal collections may be chosen freely (dict/list, etc.).
        """
        self.customers = {}
        self.suppliers = {}
        self.products = {}
        self.orders = {}
        self.orderID = 1

    def register_entity(self, entity, is_customer):
        """
        Register a Customer or Supplier in the system.

        Args:
            entity: A Customer or Supplier object.
            is_customer (bool): True if entity is Customer, False if entity is Supplier.

        Raises:
            InvalidIdException:
                - If the entity ID is invalid.
                - If the entity ID already exists in the system (note: IDs must be unique across
                  customers AND suppliers).
        """
        if is_customer:
            if entity.id in self.customers:
                raise InvalidIdException("ID already exists")
            self.customers[entity.id] = entity
        else:
            if entity.id in self.suppliers:
                raise InvalidIdException("ID already exists")
            self.suppliers[entity.id] = entity

    def add_or_update_product(self, product):
        """
        Add a new product or update an existing product.

        Behavior:
            - If product does not exist in system: add it.
            - If product exists:
                - It must belong to the same supplier as the existing one (same supplier_id),
                  otherwise raise InvalidIdException.
                - Update the stored product's fields according to the new product.

        Args:
            product: A Product object.

        Raises:
            InvalidIdException:
                - If the supplier_id does not exist in the system.
                - If attempting to update a product but supplier_id differs from the existing product.
        """
        if product.supplier_id not in self.suppliers:
            raise InvalidIdException("supplier_id does not exist")
        if product.id in self.products and self.products[product.id].supplier_id != product.supplier_id:
            raise InvalidIdException("supplier_id differs from the existing product")
        self.products[product.id] = product


    def place_order(self, customer_id, product_id, quantity=1):
        """
        Place an order for a product by a customer.

        Args:
            customer_id (int): Customer ID.
            product_id (int): Product ID.
            quantity (int, optional): Quantity to order. Defaults to 1.

        Returns:
            str: Status message according to specification:
                - "The order has been accepted in the system"
                - "The product does not exist in the system"
                - "The quantity requested for this product is greater than the quantity in stock"

        Behavior:
            - If product does not exist: return the relevant message.
            - If quantity requested > stock: return the relevant message.
            - Otherwise:
                - Decrease product stock by quantity.
                - Create a new Order with an auto-incremented system ID (starting at 1).
                - Store the order in the system.
                - Return success message.

        Notes:
            - The specification assumes quantity is an integer.
        """
        if product_id not in self.products:
            return "The product does not exist in the system"
        if self.products[product_id].quantity < quantity:
            return "The quantity requested for this product is greater than the quantity in stock"
        self.products[product_id].quantity -= quantity
        self.orders[self.orderID] = Order(self.orderID, customer_id, product_id, quantity, quantity*self.products[product_id].price)
        self.orderID += 1
        return "The order has been accepted in the system"

    def remove_object(self, _id, class_type):
        """
        Remove an object from the system by ID and type.

        Args:
            _id (int): Object ID to remove.
            class_type (str): One of: "Customer", "Supplier", "Product", "Order"
                              (exact casing/spelling per assignment).

        Returns:
            int | None:
                - If removing an Order: return the ordered quantity of that order (to restore stock).
                - Otherwise: no return value required.

        Raises:
            InvalidIdException:
                - If _id is not a valid non-negative integer.
                - If attempting to remove a Customer/Supplier/Product that still has dependent orders
                  in the system (i.e., orders that were not removed).
                - Additional InvalidIdException conditions as required by specification.
        """
        class_type = class_type.lower().strip()
        if _id < 0:
            raise InvalidIdException("Invalid id")
        if class_type == "order" and _id in self.orders:
            self.products[self.orders[_id].product_id].quantity += self.orders[_id].quantity
            order = self.orders[_id]
            del self.orders[_id]
            return order.quantity
        if class_type == "customer":
            for order in self.orders.values():
                if order.customer_id == _id:
                    raise InvalidIdException("Dependent order still exists for customer")
            if _id in self.customers:
                del self.customers[_id]
        if class_type == "product":
            for order in self.orders.values():
                if order.product_id == _id:
                    raise InvalidIdException("Dependent order still exists for product")
            if _id in self.products:
                del self.products[_id]
        if class_type == "supplier":
            for order in self.orders.values():
                if self.products[order.product_id].supplier_id == _id:
                    raise InvalidIdException("Dependent order still exists for supplier")
            if _id in self.suppliers:
                del self.suppliers[_id]
        return None

    def search_products(self, query, max_price=None):
        """
        Search products by query in the product name, and optionally filter by max_price.

        Args:
            query (str): Product name or part of product name.
            max_price (float, optional): If provided, only return products with price <= max_price.

        Returns:
            list[Product]:
                - Products that match the query and have quantity != 0,
                - Sorted by ascending price.
                - If no matching products exist, return an empty list.
        """
        products = [product for product in self.products.values() if query in product.name and product.quantity > 0]
        if max_price is not None:
            products = [product for product in products if product.price <= max_price]
        products.sort()
        return products

    def export_system_to_file(self, path):
        """
        Export system state (customers, suppliers, products) to a text file.

        Args:
            path (str): Output file path.

        Behavior:
            - Write each object on its own line, using the object's print/str representation.
            - Orders must NOT be included.
            - No constraint on the ordering of objects in the output.

        Raises:
            OSError (or any file-open exception): Must be propagated to the caller.
        """
        with open(path, "w") as f:
            for customer in self.customers.values():
                f.write(str(customer)+"\n")
            for supplier in self.suppliers.values():
                f.write(str(supplier)+"\n")
            for product in self.products.values():
                f.write(str(product)+"\n")

    def export_orders(self, out_file):
        """
        Export orders in JSON format grouped by origin city.

        Args:
            out_file (file-like)

        Behavior (per specification):
            - Produce a JSON object where:
                - Keys: origin city (supplier city) for each order.
                - Values: list of strings representing orders (format as specified in section 4.1.4).
            - Order lists can be in any order.
            - No requirement on key ordering.

        Raises:
            Any exception during writing: Must be propagated to the caller.

        Notes:
            - The order origin city is the supplier city of the ordered product.
        """
        orders = {}
        for order in self.orders.values():
            if self.suppliers[self.products[order.product_id].supplier_id].city not in orders:
                orders[self.suppliers[self.products[order.product_id].supplier_id].city] = []
            orders[self.suppliers[self.products[order.product_id].supplier_id].city].append(str(order))
        json.dump(orders, out_file)

def load_system_from_file(path):
    """
    Load a MatamazonSystem from an input file.

    Args:
        path (str): Path to a text file containing customers, suppliers and products.

    Returns:
        MatamazonSystem: Initialized system with the data found in the file.

    Behavior:
        - The file lines contain objects in the format produced by export_system_to_file (section 4.2).
        - Lines may appear in any order (e.g., product lines can appear before supplier lines).
        - Illegal lines may be ignored.
        - If an exception occurs during the creation of any required object due to invalid data,
          the function should stop and propagate the exception (as specified).

    Notes:
        - The assignment hints that eval() may be used.
    """
    system = MatamazonSystem()
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            if line[0:8] == "Customer" or line[0:8] == "Supplier":
                entity = eval(line)
                if line[0:8] == "Customer":
                    system.register_entity(entity,True)
                else:
                    system.register_entity(entity,False)
        for line in lines:
            if line[0:7] == "Product":
                system.add_or_update_product(eval(line))
    return system

# TODO all the main part here
if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 3 and len(arguments) != 5 and len(arguments) != 7 and len(arguments) != 9:
        print("Usage: python3 matamazon.py -l <matamazon_log> -s <matamazon_system> -o <output_file> -os <out_matamazon_system>", file=sys.stderr)
        exit(0)
    if "-l" not in arguments:
        print("Usage: python3 matamazon.py -l <matamazon_log> -s <matamazon_system> -o <output_file> -os <out_matamazon_system>", file=sys.stderr)
        exit(0)

    log = None
    system = MatamazonSystem()
    out = None
    out_system = None

    for i in range(1, len(arguments), 2):
        if arguments[i] == "-l":
            log = arguments[i + 1]
        elif arguments[i] == "-s":
            system = load_system_from_file(arguments[i + 1])
        elif arguments[i] == "-o":
            out = arguments[i + 1]
        elif arguments[i] == "-os":
            out_system = arguments[i + 1]

    with open(log, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            words = line.split()
            if words[0] == "register":
                if words[1] == "customer":
                    entity = Customer(int(words[2]), words[3], words[4], words[5])
                    system.register_entity(entity, True)
                else:
                    entity = Supplier(int(words[2]), words[3], words[4], words[5])
                    system.register_entity(entity, False)
            elif words[0] == "add" or words[0] == "update":
                system.add_or_update_product(
                    Product(int(words[1]), words[2], float(words[3]), int(words[4]), int(words[5])))
            elif words[0] == "order":
                if len(words) == 4:
                    system.place_order(int(words[1]), int(words[2]), int(words[3]))
                else:
                    system.place_order(int(words[1]), int(words[2]))
            elif words[0] == "remove":
                system.remove_object(int(words[2]), words[1])
            elif words[0] == "search":
                if len(words) == 3:
                    print(system.search_products(words[1], float(words[2])))
                else:
                    print(system.search_products(words[1]))

    if out is not None:
        with open(out, "w") as f:
            system.export_orders(f)
    else:
        system.export_orders(sys.stdout)

    if out_system is not None:
        system.export_system_to_file(out_system)