# 1. Write a Python program to subtract five days from current date.

# from datetime import datetime, timedelta

# c = datetime.now()
# n = c - timedelta(days=5)

# print("current:", c)
# print("-5 days:", n)



# 2. Write a Python program to print yesterday, today, tomorrow.

# from datetime import datetime, timedelta

# c = datetime.now()
# yes = c - timedelta(days=1)
# tod = c
# tom = c + timedelta(days=1)

# print("yesterday:", yes)
# print("today:", c)
# print("tomorrow:", tom)



# 3. Write a Python program to drop microseconds from datetime.

# from datetime import datetime, timedelta

# c = datetime.now()
# no_microsec = c.replace(microsecond=0)

# print(no_microsec)



# 4. Write a Python program to calculate two date difference in seconds.

# from datetime import datetime, timedelta

# # YYYY-MM-DD HH:MM:SS
# d1 = datetime(2025, 9, 2, 12, 0, 0)
# d2 = datetime(2026, 2, 24, 15, 30, 0)

# diff = abs((d2 - d1).total_seconds())

# print(int(diff))
