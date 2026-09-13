def min_coins_dp(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
      for coin in coins:
             if i >= coin:
                dp[i] = min(dp[i], 1 + dp[i - coin])
      if dp[amount] == float('inf'):
        return -1
    else:
        return dp[amount]
coins = [1, 2, 5]
amount = 11
min_coins = min_coins_dp(coins, amount)

print(f"Shivansh Darji\n230410107124")
print(f"Coin have: {coins}")
print(f"Target amount: {amount}")
print(f"Minimum number of coins required: {min_coins}")
