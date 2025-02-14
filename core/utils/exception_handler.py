from random import randint
from datetime import datetime

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response: Response = exception_handler(exc, context)

    return response


def prevent_future_date_validator(value):
    if value and value > datetime.now().date():
        raise serializers.ValidationError(
            code="nonFieldErrors",
            detail="future  date not allowed",
        )


def prevent_past_date_validator(value):
    if value and value < datetime.now().date():
        raise serializers.ValidationError(
            code="nonFieldErrors",
            detail="past date not allowed",
        )


def percentage_validator(value):
    if value != 0 and (value < 1 or value > 100):
        raise serializers.ValidationError(
            code="nonFieldErrors",
            detail="Ensure this value is between 1 and 100.",
        )


def random_with_N_digits(no_digits):
    range_start = 10 ** (no_digits - 1)
    range_end = (10**no_digits) - 1
    return randint(range_start, range_end)
