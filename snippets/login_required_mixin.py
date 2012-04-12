# !title: Login requied mixin for Django class-based views.
# !date: 2012-04-12
# !tags: Django, CBV
# !author: Dima Kukushkin

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
