import re

# Найти все действительные числа, например: -100; 21.4; +5.3; -1.5; 0
res = re.findall(r"[-+]?\d+(?:\.\d+)?", test_str)


# Проверить, что строка это серийный номер вида 00XXX-XXXXX-XXXXX-XXXXX, где X - шестнадцатиричная цифра
if re.match(r"^00[\da-f]{3}(?:-[\da-f]{5}){3}$", serial_str, re.IGNORECASE):
    pass

# Проверить, что строка является корректным IPv4 адресом
if re.match(r"^((25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(\.|$)){4}(?<!\.)$", ip_str):
    pass

# Проверить, что логин содержит от 8 до 16 латинских букв, цифр и _
if re.match(r"^\w{8,16}$", login):
    pass

# Проверить, что пароль состоит не менее чем из 8 символов без пробелов. Пароль должен содержать хотя бы одну: строчную букву, заглавную, цифру
if re.match(r"^(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])\S{8,}$", password):
    pass
  
# Переформатировать код, убрав лишние пробелы между def, именем функции и (
# Например: def    myFunc   (x, y):  => def myFunc(x, y):
re.sub(r'def\s+(\w+)\s*\(', r'def \1(', code)


#Заменить все "camel_case" на "сamelCase"
# Например: my_function_name, peer__2__peer  =>  myFunctionName, peer2Peer
re.sub('_+([a-zA-Z\d])', lambda x: x.group(1).upper(), code.lower())
