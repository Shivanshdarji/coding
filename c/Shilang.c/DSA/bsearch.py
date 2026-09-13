def binary_search(arr, low, high, target):
    while low <= high:
        middle = (low + high) // 2
        if arr[middle] == target:
            return middle
        elif arr[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1

list3 = [1, 2, 55, 66, 77, 81, 90, 344]
target = 55
res = binary_search(list3, 0, len(list3) - 1, target)

print("Shivansh Darji\n230410107124")
print(f"Searching for {target} using Binary Search")

if res != -1:
    print("Element found at index", res)
else:
    print("Element not found")
