#1
#from datetime import datetime, timedelta

# берем текущую дату и время
current_date = datetime.now()

# создаем объект timedelta на 5 дней
five_days = timedelta(days=5)

# вычитаем 5 дней
new_date = current_date - five_days

print("Current date:", current_date)
print("5 days ago:", new_date)

#2

from datetime import datetime, timedelta

today = datetime.now()

yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#3

from datetime import datetime

now = datetime.now()

# replace заменяет микросекунды на 0
without_microseconds = now.replace(microsecond=0)

print("With microseconds:", now)
print("Without microseconds:", without_microseconds)

#4

from datetime import datetime

# пример дат
date1 = datetime(2026, 2, 20, 12, 0, 0)
date2 = datetime(2026, 2, 23, 12, 0, 0)

# разница — это timedelta
difference = date2 - date1

# переводим в секунды
seconds = difference.total_seconds()

print("Difference in seconds:", seconds)



