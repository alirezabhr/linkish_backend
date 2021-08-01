import random
import string
import django.utils.timezone as django_tz
from geoip2.webservice import Client


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
    now = django_tz.now()
    timedelta_per_second = (now-time).total_seconds()
    if timedelta_per_second/(3600*24) > 1:
        return True
    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_in_iran(ip):
    client = Client(589085, 's9lO8TbLzvP03RjD', host='geolite.info')
    country = client.country(ip)
    if country.country.iso_code == 'IR':
        return True
    return False
