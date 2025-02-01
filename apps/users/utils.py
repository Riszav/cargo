import random
import string


def generate_client_id():
    client_id = ''.join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(0, 999)).zfill(3)
    return client_id