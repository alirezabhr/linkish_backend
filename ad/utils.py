import random
import string


def generate_random_string(size=6, chars=string.ascii_letters + string.digits):
    new_str = ''
    for _ in range(size):
        new_str += random.choice(chars)
    return new_str


def get_random_link(instance, size=6):
    new_str = generate_random_string(size=size)

    qs_exists = instance.objects.filter(short_link=new_str).exists()
    if qs_exists:
        return get_random_link(instance=instance, size=size)

    return new_str


def is_after_24h(time):
    print(time)
