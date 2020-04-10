import factory
import pytest
from django.contrib.auth.models import Permission, User
from django.urls import reverse

from patterns.models import Pattern, PatternStatus


class PatternStatusFactory(factory.DjangoModelFactory):
    class Meta:
        model = PatternStatus


@pytest.mark.django_db
def test_url_pattern_card(client):
    pattern1 = Pattern.objects.create(status=PatternStatusFactory())
    response = client.get(reverse("patterns:pattern-card", args=[pattern1.pk]))
    assert list(response.context["objects"]) == []
    assert response.status_code == 200


@pytest.mark.django_db
def test_url_pattern(client):
    assert client.get(reverse("patterns:patterns")).status_code == 200
    assert client.get(f"/patterns/api/patterns/").status_code == 200


@pytest.mark.django_db
def test_url_pattern_card(client):
    pattern1 = Pattern.objects.create(status=PatternStatusFactory())
    response = client.get(reverse("patterns:pattern-card", args=[pattern1.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_url_pattern_create(client):
    assert client.get(reverse("patterns:pattern-create")).status_code == 302

    user1 = User.objects.create_user(username="modelarnia", password="test_password")
    client.login(username="modelarnia", password="test_password")
    assert client.get(reverse("patterns:pattern-create")).status_code == 403

    perm_add_pattern = Permission.objects.get(codename="add_pattern")
    user1.user_permissions.add(perm_add_pattern)
    assert client.get(reverse("patterns:pattern-create")).status_code == 200


@pytest.mark.django_db
def test_url_pattern_report(client):
    response = client.get(reverse("patterns:pattern-report"))
    assert response.status_code == 200
    response = client.post(reverse("patterns:pattern-report"), {"customer1": "test"})
    assert response.status_code == 200
