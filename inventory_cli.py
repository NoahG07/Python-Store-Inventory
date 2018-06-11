#!/usr/bin/env python3
# 
# Program to keep track of your inventory for personal sites, yard sales, etc.

def banner():
    the_menu = """\nWelcome, what would you like to:
    1) Add to inventory
    2) Remove from inventory
    3) Update inventory
    4) Check the Inventory
    5) Exit
    """
    print(the_menu)

def menu(c):
    try:
        choice = int(input("\n> "))
        if choice == 1:
            add_inventory(conn, c)
        if choice == 2:
            remove_inventory(conn, c)
        if choice == 3:
            update_inventory(c)
        if choice == 4:
            read_inventory(conn, c)
            #print(read_inventory(conn, c))
        if choice == 5:
            exit()
                    
    except (ValueError, KeyboardInterrupt) as e:
        print(e)
        exit()

def add_inventory(conn, c):
    add_item = str(input("Enter item: "))
    add_quantity = int(input("Quantity: "))
    add_price = float(input("Asking Price: $"))
    
    with conn:
        c.execute("INSERT INTO decor VALUES(:item, :quantity, :price)", {
            "item":add_item,
            "quantity":add_quantity,
            "price":add_price
        })
    read_inventory(conn, c)
    #print(read_inventory(conn, c))

def remove_inventory(conn, c):
    sold = input("What was sold? ")
    with conn:
        c.execute("DELETE FROM decor WHERE Item=:item", {"item":sold})
    read_inventory(conn, c)
    #print(read_inventory(conn, c))
        
def read_inventory(conn, c):
    with conn:
        search = c.execute("SELECT * FROM decor")
        print("\nItem ---- Qt. ---- Price")
        for row in search:
            print(row)
            #return row
    
def update_inventory(c):
    read_inventory(conn, c)
    what_item = input("What item changed? ")
    quant = input("Did the quantity change? (yes/no) ")
    if quant.lower() == "yes":
        how_many = int(input("New Quantity: "))
        c.execute("UPDATE decor SET Quantity=:quanti WHERE Item=:items", {
            "quanti":how_many,
            "items":what_item
        })
        read_inventory(conn, c)
        #print(read_inventory(conn, c))
    else:
        prices = input("Did price change? (yes/no) ")
        if prices.lower() == "yes":
            new_price = float(input("New Price: $"))
            c.execute("UPDATE decor SET Price=:prices WHERE Item=:items", {
            "prices":new_price,
            "items":what_item
            })
            read_inventory(conn, c)
            #print(read_inventory(conn, c))        
        else:
            print("Nothing to change.")
            exit

if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS decor(
            Item text,
            Quantity integer,
            Price real
            ) """)
    banner()
    while True:
        menu(c)
