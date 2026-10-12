from django.utils import translation


class UserLanguageMiddleware:
    # Para un usuario con sesión iniciada se usa el idioma guardado en su cuenta (es o en)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            translation.activate(request.user.language)
            request.LANGUAGE_CODE = request.user.language
        return self.get_response(request)
