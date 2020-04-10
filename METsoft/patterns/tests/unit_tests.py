import datetime
from unittest import mock

import pytest
from django.urls import reverse

from patterns.models import Pattern, PatternStatus


@pytest.fixture(name="pattern_status")
def fixture_pattern_status():
    status = PatternStatus()
    return status


@pytest.fixture(name="pattern")
def fixture_pattern(pattern_status):
    pattern = Pattern()
    pattern.status = pattern_status
    return pattern


def test_pattern_status_str(pattern_status):
    pattern_status.status = "test"
    assert str(pattern_status) == pattern_status.status


def test_pattern_str(pattern):
    pattern.pattern_name = "test"
    assert str(pattern) == pattern.pattern_name


def test_pattern_get_absolute_url(pattern):
    assert pattern.get_absolute_url() == reverse("patterns:patterns")


def test_pattern_get_not_using_time_if_status_id_is_true(pattern):
    pattern.status.pk = 4
    assert pattern.get_not_using_time() is None


@pytest.mark.parametrize("days, expected", [(365, 12), (29, 0), (30, 1)])
def test_pattern_get_not_using_time_if_last_order_is_true(pattern, days, expected):
    pattern.last_order = datetime.date.today() - datetime.timedelta(days=days)
    assert pattern.get_not_using_time() == expected


def test_pattern_get_not_using_time_if_last_order_is_false(pattern):
    pattern.last_order = None
    assert pattern.get_not_using_time() is None


@mock.patch("patterns.models.Pattern.add_status_to_pattern_history")
@mock.patch("patterns.models.Pattern.patternhistory_set")
def test_if_status_changed_update_history_if_statement_true(
    mock_patternhistory, mock_add_status, pattern, pattern_status
):
    pattern.if_status_changed_update_history()
    mock_add_status.assert_called_once()


def test_if_status_change_update_history_if_statement_false():
    pass


@mock.patch("patterns.models.PatternHistory.objects.create")
def test_pattern_add_status_to_pattern_history(mock_pattern_history, pattern):
    pattern.add_status_to_pattern_history()
    mock_pattern_history.assert_called_once()
