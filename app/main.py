import controllers
import models

def manage_table_menu():
    while True:
        print("\n--- Table Management ---")
        print("1. Add a new table")
        print("2. Remove a table")
        print("3. Back to main menu")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            controllers.add_table()
        elif choice == 2:
            table_number = int(input("plz enter table number you want to remove: "))
            controllers.remove_table(table_number)
        elif choice == 3:
            print("directing to main menu...")
            break
        else:
            print("invalid choice! plz try again.")
            continue


def main_menu():
    while True:
        print("---Restaurant Management System---")
        print("1. Show Menu")
        print("2. Show Table Status")
        print("3. Add New Order")
        print("4. Update Order Status")
        print("5. View Order Details & Total Price")
        print("6. Show Daily Sales Report")
        print("7. Manage Tables")
        print("8. Add new menu item")
        print("9. Exit")

        choice = int(input("enter your choice: "))

        if choice == 1:
            controllers.show_menu()
            continue
        elif choice == 2:
            controllers.show_tables()
            continue
        elif choice == 3:
            table_number = int(input("Enter the table number for order: "))

            new_order = controllers.add_order(table_number)

            if not new_order:
                print("Failed to create order.")
                continue

            while True:
                add_more = input("Do you want to add an item to this order? (y/n): ").lower()
                if add_more != 'y':
                    break

                item_id = int(input("Enter menu item id: "))
                quantity = int(input("Enter quantity: "))

                controllers.add_order_detail(new_order.id, item_id, quantity)
        elif choice == 4:
            order_id = int(input("enter the order id: "))
            status_input = (input("enter new order status: pending, done or canceled")).lower()
            try:
                order_status = models.OrderStatus(status_input)
                controllers.update_order_status(order_id, order_status)
            except ValueError:
                print("Invalid status! plz enter pending, done or canceled.")
            continue
        elif choice == 5:
            order_id = int(input("enter id of the order you want to see details: "))
            controllers.show_order_details(order_id)
            continue
        elif choice == 6:
            controllers.get_today_sales_report()
            continue
        elif choice == 7:
            manage_table_menu()
            continue
        elif choice == 8:
            item_name = input("plz enter item name: ")
            item_price = input("plz enter item price: ")
            quantity = int(input("plz enter amount of the item: "))
            controllers.add_menu_item(item_name, item_price, quantity)
            continue
        elif choice == 9:
            print("Goodbye!")
            break
        else:
            print("invalid choice! plz try again.")
            continue



if __name__ == "__main__":
    main_menu()