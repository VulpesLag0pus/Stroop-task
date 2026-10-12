from vending_tools import is_valid_code, in_stock, format_price, coins_for_change, best_seller
# the machine code that was given 
machine = {
    "A1": {"name": "Stroopwafels",        "price": 150, "stock": 10},
    "A2": {"name": "Instant Noodles",     "price": 120, "stock": 10},
    "B1": {"name": "Energy Drink",        "price": 250, "stock": 10},
    "B2": {"name": "Emergency Chocolate", "price": 185, "stock": 10},
    "C1": {"name": "Mystery Snack",       "price": 95,  "stock": 10},
    "C2": {"name": "Coke Zero",           "price": 210, "stock": 10},
}

def show_menu(machine:dict) -> None:   #;takes the machine dictionaru and means it returns nothing
    print("=" * 44)
    print("     THE HUNGRY STUDENT VENDING MACHINE")
    print("=" * 44)
    for code, slot in machine.items():     #takes each pair from the dictionary one at a time
        if in_stock(code, machine):
            price = format_price(slot["price"]) #in teh price place replace with teh price given above, if not replace slot with sold out
        else:
            price = "SOLD OUT"
        print(f" {code} {slot['name']:<20} {price}") #this prints the menu line from the machine code above

def run_machine(machine:dict)-> None:
    total_cents = 0 
    sales = {}
    while True:  #reapets till something stops the loop
        show_menu(machine)
        choice = input("\nPick a code (or q to quit):").strip() #strip() removes accidental spaces
       
        if choice.lower() =="q": #is the quit path causeing the loop to stop, lower is used so both Q and q work
            print(f"Session total: {format_price(total_cents)}")
            print(f"Best seller: {best_seller(sales)}")
            print("The machine hums contentedly. Bye!") 
            break

        if not is_valid_code(choice, machine): # if the code is not rea, then it will print the message below and restart the loop
            print("that code doesn't exist. \n") #\n ends the current line and starts a new one
            continue
            
        code = choice.upper() # makes version such as a1 become A1s to stay consistent in teh dictionary

        if not in_stock(code, machine): #if the item has no stock/ less then 0 then it will print this message 
            print(f"sorry, {machine[code]['name']} is sold out.\n")
            continue

        slot = machine[code] #grabs from the dictonary for the slot
        price = slot["price"]
        print(f"{slot['name']} costs {format_price(price)}")

        paid = int(input("Insert money(in cents):")) #coverts user text into whole number of cents

        if paid < price:
            missing = price - paid
            print(f"Not enough money. You are {format_price(missing)} short.") 
            continue

        slot["stock"] -= 1  # deletes one from the stock when ordered
        total_cents += price #adds this snak price to the total
        sales[slot["name"]] = sales.get(slot["name"], 0) +1 #gives the current count or 0 i no snacks have been sold
        print(f"Enjoy your {slot['name']}!")

        change = paid - price
        if change == 0:
            print("Exact payment You're awesome. \n")
        else: 
            print(F"Change: {format_price(change)}")
            coins = coins_for_change(change)
            for coin, count in coins.items():
                print(f"{count} x {format_price(coin)}")
            print()
run_machine(machine)