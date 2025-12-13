import database
import models
from sqlalchemy import func

# menu management
# =========================================
def add_menu_item(item_name, item_price, quantity):
    try:
        new_item = models.MenuItem(name=item_name, price=item_price, quantity=quantity)
        database.session.add(new_item)
        database.session.commit()
        print(f"Menu item '{item_name}' added successfully.")
    except Exception as e:
        print(f"An error occurred while adding the menu item: {e}")
        database.session.rollback()


def edit_menu_item_price(item_name, new_price):
    try:
        menu_item = database.session.query(models.MenuItem).filter_by(name=item_name).first()
        if menu_item:
            menu_item.price = new_price
            database.session.commit()
            print(f"Price of '{item_name}' updated successfully.")
        else:
            print(f"Menu item '{item_name}' not found.")
    except Exception as e:
        print(f"An error occurred while updating the price: {e}")
        database.session.rollback()


def show_menu():
    menu_items = database.session.query(models.MenuItem).all()
    for item in menu_items:
        print(item)

# table management
# =========================================
def show_tables():
    tables = database.session.query(models.Table).all()
    for table in tables:
        print(table)


def update_table_status(table_number, new_status: bool):
    try:
        table = database.session.query(models.Table).filter_by(table_number=table_number).first()
        if table:
            table.status = new_status
            database.session.commit()
            print(f"Table {table_number} status updated to {new_status}.")
        else:
            print(f"Table {table_number} not found.")
    except Exception as e:
        print(f"An error occurred while updating the table status: {e}")
        database.session.rollback()


def add_table():
    try:
        new_table = models.Table()
        database.session.add(new_table)
        database.session.commit()
        print("New table added successfully.")
    except Exception as e:
        print(f"An error occurred while adding the table: {e}")
        database.session.rollback()


def remove_table(table_number):
    try:
        table_to_delete = database.session.query(models.Table).filter_by(table_number=table_number).first()
        if table_to_delete:
            database.session.delete(table_to_delete)
            database.session.commit()
            print(f"Table {table_number} removed successfully.")
        else:
            print(f"Table {table_number} not found.")
    except Exception as e:
        print(f"An error occurred while removing the table: {e}")
        database.session.rollback()

#order management
# =========================================
def add_order(table_number, status="pending"):
    try:
        table = database.session.query(models.Table).filter_by(table_number=table_number).first()

        if table:
            new_order = models.Order(table_id=table.id, status=status)
            database.session.add(new_order)
            database.session.commit()
            print(f"New order created for table number {table_number}")
        else:
            print(f"Table number {table_number} not found.")
    except Exception as e:
        print(f"An error occurred while adding the order: {e}")
        database.session.rollback()


def update_order_status(order_id, new_status):
    try:
        order = database.session.query(models.Order).filter_by(id=order_id).first()
        if order:
            order.status = new_status
            print("status updated")
        else:
            print(f"order number {order_id} not found!")
    except Exception as e:
        print(f"An error occurred while updating the status: {e}")

#report
#=================================================
def show_active_orders():
    orders = database.session.query(models.Order).filter(status="pending").all()
    for order in orders:
        print(order)


def show_order_details(order_id):
    try:
        order_details = database.session.query(models.Order, models.OrderDetails, models.MenuItem) \
            .join(models.OrderDetails, models.OrderDetails.order_id == models.Order.id) \
            .join(models.MenuItem, models.MenuItem.id == models.OrderDetails.item_id) \
            .filter(models.Order.id == order_id) \
            .all()

        if not order_details:
            print(f"No order found with ID {order_id}.")
            return

        print(f"Order ID: {order_id}")
        for order, order_detail, menu_item in order_details:
            total_price = order_detail.quantity * menu_item.price
            print(f"Item: {menu_item.name}, Quantity: {order_detail.quantity}, "
                  f"Price per Item: {menu_item.price}, Total Price: {total_price}")

    except Exception as e:
        print(f"An error occurred: {e}")


def get_daily_sales_report(date):
    try:
        daily_sales = database.session.query(
            func.sum(models.OrderDetails.quantity * models.MenuItem.price).label("total_sales")) \
            .join(models.MenuItem, models.MenuItem.id == models.OrderDetails.item_id) \
            .join(models.Order, models.Order.id == models.OrderDetails.order_id) \
            .filter(func.date(models.Order.order_time) == date) \
            .scalar()

        if daily_sales is None:
            print(f"No sales found for {date}.")
            return

        print(f"Total sales for {date}: {daily_sales} units sold.")

    except Exception as e:
        print(f"An error occurred: {e}")
