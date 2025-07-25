from django.shortcuts import redirect
from functools import wraps

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        # Se não está logado, manda para login
        if not user.is_authenticated:
            return redirect('login')

        # Senão, executa a view normalmente
        return view_func(request, *args, **kwargs)

    return wrapper