# 1 Extract all prices from the receipt

# import re
# from pathlib import Path

# pth = Path(__file__).with_name("raw.txt")
# text = pth.read_text(encoding="utf-8")

# pattern = re.compile(r"^Стоимость\s*\r?\n(?P<Price>\d+[0-9 ]*,\d{2})$", re.MULTILINE)

# m = pattern.findall(text)

# for i in m:
#     print(i)






# 2 Find all product names

# import re
# from pathlib import Path

# product_pattern = re.compile(
# 	r"^\d+\.\s*\n"
# 	r"(?P<name>.*?)\n",
# 	re.MULTILINE,
# )

# def getnames(text: str) -> list[str]:
# 	return [m.group("name").strip() for m in product_pattern.finditer(text)]


# pth = Path(__file__).with_name("raw.txt")
# text = pth.read_text(encoding="utf-8")
# product_names = getnames(text)

# for i, name in enumerate(product_names, start=1):
# 	print(f"{i}. {name}")




# 3 Calculate total amount


# import re
# from pathlib import Path

# amount_pattern = re.compile(
# 	r"^ИТОГО:\s+(?P<tot_amount>[\d\s,]+)",
# 	re.MULTILINE,
# )

# def to_num(value: str) -> float:
#     return float(value.replace(" ", "").replace(",", "."))

# def total_amount_of_products(text: str) -> float:
#     match = amount_pattern.search(text)
#     if not match:
#         print("Amount was not found")
#         return -1.0
    
#     amount_str = match.group("tot_amount")
#     return to_num(amount_str)

# pth = Path(__file__).with_name("raw.txt")
# text = pth.read_text(encoding="utf-8")

# total_amount = total_amount_of_products(text)
# print(f"Total amount of products: {total_amount}")





# 4 Extract date and time information

# import re
# from pathlib import Path

# pth = Path(__file__).with_name("raw.txt")
# text = pth.read_text(encoding="utf-8")

# date_time_pattern = re.compile(r"Время:\s*(?P<date>\d{2}\.\d{2}\.\d{4})\s+"
#                                r"(?P<time>\d{2}:\d{2}:\d{2})")

# m = re.search(date_time_pattern, text)

# if m:
#     date, time = m.group("date"), m.group("time")
#     print(date,time)
# else:
#     print("Not found")



# 5 Find payment method
# import re
# from pathlib import Path

# pth = Path(__file__).with_name("raw.txt")
# text = pth.read_text(encoding="utf-8")

# payment_method_pattern = re.compile(r"^(?P<method>Банковская карта|Наличные):\s*$", 
#                                     re.MULTILINE)

# m = re.search(payment_method_pattern, text)

# if m:
#     print(m.group("method"))
# else:
#     print("Not found")






# example with finding words with letter т
# import re
# from pathlib import Path

# pth = Path(__file__).with_name("raw.txt")
# text = pth.read_text(encoding="utf-8")

# pattern = re.compile(r"\b\w*т\w*\b", re.IGNORECASE)


# print(pattern.findall(text))



# example with finding any word which contains a number 
# import re
# from pathlib import Path

# pth = Path(__file__).with_name("raw.txt")
# text = pth.read_text(encoding="utf-8")

# pattern = re.compile(r"\b\S*\d\S*\b", re.IGNORECASE)


# print(pattern.findall(text))


