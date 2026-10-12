def is_valid_code(code: str,machine: dict)-> bool:  #checks for valid cod
    """Return True if code is a real slot in the machine"""
    return code.upper() in machine #turns responses such as a1 into A1

def in_stock(code: str, machine:dict)-> bool: #checks whether it is in stock
    """Return True if the slot has at least one item."""
    return machine[code.upper()]["stock"] > 0
## True only if the slot has at least one item left (stock above 0)

def format_price(cents: int)-> str: #puts units of cents and makes into euro string
    """Convert cents to a euro, e.g. 150 -> '1.50'."""
    euros = cents //100 #takes the integer and divides it by 100 and gets rid of everything after the decimal point
    rest = cents % 100 # % repersents the remainder of the previouse division
    return f"{euros}.{rest:02d}"  #turns it into an f string, thus what is inside the bracket is replaced by the value of the variable
#combine teh the whole interger, euro, with the remainder, rest 
# 02d means the whole number with at leats two characters and if not large enough replace with zeros

def coins_for_change(cents:int)-> dict:
    """Return the fewest coins for the change as {coin: count}."""
    result = {}     #starts an empty dictionary, to fill with coins
    for coin in [200, 100, 50, 20, 10, 5]:  #makes a list of coins biggest to smallest, thus using biggest coins first
        count = cents // coin   #divides cents by coins to show how many coins still need to pay, thus drops teh decimal
        if count > 0:   # skips coins yu do not use, thus only showing what coins have been used 
            result[coin] = count #this coin gives this many 
            cents = cents % coin #addsthe remainder
    return result
#reduces the amount of cents into fewer coins

def best_seller(sales: dict) -> str:
    """The snack with the most stock sold"""
    if not sales:
        return "nothing is sold yet"
    return max(sales, key=sales.get) #compares them by their values through the dictionary snack names

if __name__ == "__main__":
    machine = {
        "A1": {"name": "Stroopwafels",        "price": 150, "stock": 1},
        "A2": {"name": "Instant Noodles",     "price": 120, "stock": 10},
        "B1": {"name": "Energy Drink",        "price": 250, "stock": 10},
        "B2": {"name": "Emergency Chocolate", "price": 185, "stock": 0},
        "C1": {"name": "Mystery Snack",       "price": 95,  "stock": 10},
        "C2": {"name": "Coke Zero",           "price": 210, "stock": 10},
    }
    assert is_valid_code("A1", machine) == True
    assert is_valid_code("a1", machine) == True
    assert is_valid_code("Z9", machine) == False
    assert in_stock("A1", machine) == True
    assert in_stock("B2", machine) == False
    assert format_price(150) == "1.50"
    assert format_price(5) == "0.05"
    assert format_price(0) == "0.00"
    assert coins_for_change(285) == {200: 1, 50: 1, 20: 1, 10: 1, 5: 1}
    assert coins_for_change(400) == {200: 2}
    assert coins_for_change(80) == {50: 1, 20: 1, 10: 1}
    assert coins_for_change(0) == {}
    assert best_seller({"Stroopwafels": 3, "Coke Zero": 1}) == "Stroopwafels"
    assert best_seller({"Energy Drink": 1, "Mystery Snack": 4}) == "Mystery Snack"
    assert best_seller({}) == "nothing is sold yet"

    print("vending_tools: all tests passed!")