def calculate_profit(sales, costs, tax_rate=0.10):
    profit = sales - costs
    profit -= profit * tax_rate 
    return profit

print(calculate_profit(1000, 600))  # Example usage