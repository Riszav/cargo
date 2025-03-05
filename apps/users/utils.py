import random
import string


# def generate_client_id():
#     client_id = ''.join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(0, 999)).zfill(3)
#     return client_id

# def generate_client_id(latest=None):
#     if latest:
#         last_client_id = latest.client_id
#         last_client_id = last_client_id.split(2)
#         last_client_id = last_client_id[0] + str(int(last_client_id[1]) + 1).zfill(3)
#         client_id = last_client_id
#     else:
#         client_id = "AA001"
#     return client_id


import string

def increment_client_id(client_id):
    letters, numbers = client_id[:2], int(client_id[2:])
    
    # Увеличиваем число
    numbers += 1
    if numbers > 999:
        numbers = 1  # Сбрасываем счетчик чисел
        letters = increment_letters(letters)  # Увеличиваем буквы
    
    return f"{letters}{numbers:03d}"

def increment_letters(letters):
    # Преобразуем буквы в числовой индекс (AA → AB → ... → ZZ)
    letter1, letter2 = letters
    alphabet = string.ascii_uppercase
    
    if letter2 == 'Z':  
        if letter1 == 'Z':  
            return "AA"  # Если достигли ZZ, сбрасываем
        letter1 = alphabet[alphabet.index(letter1) + 1]
        letter2 = 'A'
    else:
        letter2 = alphabet[alphabet.index(letter2) + 1]
    
    return letter1 + letter2

def generate_client_id(latest):
    if latest:
        last_client_id = latest.client_id
        return increment_client_id(last_client_id)
    return "AA001"

# Пример работы:
class FakeLatest:
    def __init__(self, client_id):
        self.client_id = client_id

latest = FakeLatest("AA001")
print(generate_client_id(latest))  # Должно вывести "BA001"
