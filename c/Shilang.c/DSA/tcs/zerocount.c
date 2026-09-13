#include <stdio.h>

int main() {
    long long L, K;
    scanf("%lld %lld", &L, &K);

    // Base cases
    if (K == 0) {
        printf("%lld", L); // All zeros
        return 0;
    }
    
    if (K == L) {
        printf("0"); // All ones, no zeros
        return 0;
    }

    // Calculate number of zeros and gaps
    long long Z = L - K; // Total zeros
    long long G = K + 1; // Number of gaps

    long long zeros_per_gap = Z / G; // Basic distribution
    long long extra_zeros = Z % G;    // Extra zeros to distribute

    // Longest block of zeros
    long long longest_zeros = zeros_per_gap + (extra_zeros > 0 ? 1 : 0);

    printf("%lld", longest_zeros);
    return 0;
}
