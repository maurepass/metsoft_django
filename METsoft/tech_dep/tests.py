from datetime import timedelta, date

import pytest
from django.contrib.auth.models import User

from .models import Order, OrderStatus


@pytest.fixture(name="tech_memb")
def fixture_tech_memb():
    tech_memb = User(username="test_user")
    return tech_memb


@pytest.fixture(name="status")
def fixture_status():
    status = OrderStatus(status="test_status")
    return status


@pytest.fixture(name='order')
def fixture_order(tech_memb, status):
    order = Order(
        numer_met="test_met",
        company="test_company",
        cast_name="test_cast_name",
        tech_memb=tech_memb,
        status=status,
    )
    return order


def test_order_status_str(status):
    assert str(status) == status.status


def test_order_str(order):
    assert str(order) == f"{order.numer_met} {order.company} {order.cast_name} {order.tech_memb} {order.status}"


def test_get_working_time_if_false(order):
    order.working_time = 100
    assert order.get_working_time() == order.working_time


def test_get_working_time_if_true(order):
    order.ord_in = date.today() - timedelta(days=30)
    order.status.pk = 2
    assert order.get_working_time() == 30
