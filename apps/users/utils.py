import random
import string

# def generate_client_id():
#     client_id = ''.join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(0, 999)).zfill(3)
#     return client_id


import string

def increment_client_id(client_id):
    letters, numbers = client_id[:2], int(client_id[2:])
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

def generate_client_id(latest, model):
    if latest.client_id:
        client_id = increment_client_id(latest.client_id)
        while model.objects.filter(client_id=client_id).exists():
            client_id = increment_client_id(client_id)
        return client_id
    return "AA001"

# # Пример работы:
# class FakeLatest:
#     def __init__(self, client_id):
#         self.client_id = client_id

# latest = FakeLatest("AA001")
# print(generate_client_id(latest))  # Должно вывести "BA001"
