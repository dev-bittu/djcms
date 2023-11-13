from django.shortcuts import redirect
from django.contrib import messages

class ManagementAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/manage/'):
            if request.user.is_anonymous or not request.user.is_author:
                messages.warning(request, "Not authorized to access the page")
                return redirect("index")
        return self.get_response(request)
