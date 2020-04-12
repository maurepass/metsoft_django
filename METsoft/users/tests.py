from django.contrib.auth.models import User


def test_user_get_first_name():
    user = User(username='test_user', first_name='test fist name')
    assert str(user) == user.first_name
