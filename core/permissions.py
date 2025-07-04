from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def max_authorization(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.info(
                request, "Only users with authorization can perform this task."
            )
            return redirect("core:sales")
        return func(request, *args, **kwargs)
    return wrapper


def is_logged_in(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(
                request, "You are already logged in, you can't log in twice."
            )
            return redirect("core:sales")
        return func(request, *args, **kwargs)
    return wrapper
