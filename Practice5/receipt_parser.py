import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()

# 1) date/time
dt = None
m = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
if m:
    dt = {"date": m.group(1), "time": m.group(2)}

# 2) payment method + amount
payment_method = None
payment_amount = None
for i, line in enumerate(lines):
    if line.strip().startswith("Банковская карта"):
        payment_method = "Банковская карта"
        if i + 1 < len(lines):
            m2 = re.search(r"\d[\d\s]*,\d{2}", lines[i + 1])
            if m2:
                payment_amount = float(m2.group(0).replace(" ", "").replace(",", "."))
        break

# 3) items (очень простой парсинг: номер -> следующая строка это имя)
items = []
for i in range(len(lines) - 1):
    if re.fullmatch(r"\s*\d+\.\s*", lines[i]):
        name = lines[i + 1].strip()
        items.append(name)

# 4) totals (берём суммы ПОСЛЕ слов "Стоимость")
money_strings = re.findall(r"Стоимость\s*\n\s*(\d[\d\s]*,\d{2})", text)
line_totals = [float(x.replace(" ", "").replace(",", ".")) for x in money_strings]
computed_total = sum(line_totals)

# 5) receipt total (ИТОГО -> следующая строка)
receipt_total = None
m3 = re.search(r"ИТОГО:\s*\n\s*(\d[\d\s]*,\d{2})", text)
if m3:
    receipt_total = float(m3.group(1).replace(" ", "").replace(",", "."))

data = {
    "datetime": dt,
    "payment": {"method": payment_method, "amount": payment_amount},
    "items": items,
    "totals": {"computed_total": computed_total, "receipt_total": receipt_total},
}

print(json.dumps(data, ensure_ascii=False, indent=2))