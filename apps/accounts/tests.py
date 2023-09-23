import random
from faker import Faker
from .models import CustomUser
from ..profiles.models import Friend

fake = Faker('ru_RU')  # Для русских данных


# Генерация случайного пароля
def generate_password():
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    password = ''.join(random.choice(characters) for _ in range(12))
    return password


# Генерация пользователей
def generate_users(num_users):
    users = []
    for _ in range(num_users):
        user = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'username': fake.user_name(),
            'phone_number': fake.phone_number(),
            'bio': fake.text(),
            'birthdate': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
            'password': generate_password(),
        }
        users.append(user)
    return users


# use = generate_users(500)
# for i in use:
#     a = CustomUser.objects.create(**i)
#     if a:
#         print('Created new user', a.username)

user = CustomUser.objects.get(id=1)
for i in range(10, 20):
    friend = CustomUser.objects.get(id=i)
    Friend.objects.create(user=friend, friend=user)
