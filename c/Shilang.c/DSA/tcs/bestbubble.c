#include <stdio.h>

int count_swaps(int arr[], int n, int order) {
    int swaps = 0;

    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if ((order == 1 && arr[i] > arr[j]) || (order == -1 && arr[i] < arr[j])) {
                swaps++;
            }
        }
    }

    return swaps;
}

int main() {
    int n;
    scanf("%d", &n);

    int arr[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    int ascending_swaps = count_swaps(arr, n, 1);
    int descending_swaps = count_swaps(arr, n, -1);

    int min_swaps = (ascending_swaps < descending_swaps) ? ascending_swaps : descending_swaps;
    printf("%d", min_swaps);

    return 0;
}