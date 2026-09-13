def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

list2 = [1, 34, 12, 32, 67, 89, 10, 55]
target = 67
tar = linear_search(list2, target)

print("Shivansh Darji\n230410107124")
print(f"Searching for {target}")

if tar != -1:
    print("Element found at index", tar)
else:
    print("Element not found")
