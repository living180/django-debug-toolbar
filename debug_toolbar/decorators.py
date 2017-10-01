import functools

from django.http import Http404


def require_allow_toolbar(view):
    @functools.wraps(view)
    def inner(request, *args, **kwargs):
        from debug_toolbar.middleware import get_allow_toolbar

        allow_toolbar = get_allow_toolbar()
        if not allow_toolbar(request):
            raise Http404

        return view(request, *args, **kwargs)

    return inner
