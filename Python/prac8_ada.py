def fractional_knapsack(items, capacity):
   
    for i in range(len(items)):
        items[i] = (items[i][0] / items[i][1], items[i][0], items[i][1])  # (ratio, value, weight)

    items.sort(key=lambda x: x[0], reverse=True)

    total_value = 0.0
    items_taken = []
    
    for ratio, value, weight in items:
        if capacity == 0:
            break
        
        if weight <= capacity:
            total_value += value
            capacity -= weight
            items_taken.append(f"Full item (Value: {value}, Weight: {weight})")
      
        else:
            fraction = capacity / weight
            total_value += value * fraction
            items_taken.append(f"Fractional item (Value: {value}, Weight: {weight}, Fraction: {fraction:.2f})")
            capacity = 0 
            
    return total_value, items_taken


items = [(60, 10), (100, 20), (120, 30)]
capacity = 50

max_value, taken_items = fractional_knapsack(items, capacity)

print(f"Shivansh Darji\n230410107124")
print(f"Items: {items}")
print(f"Knapsack capacity: {capacity}")
print(f"\nMaximum value using greedy approach: {max_value:.2f}")
print("Items taken:")

for item in taken_items:
    print(f"- {item}")
