from django.utils import timezone

from apps.company.models import PlanLog, Rule, RequestLog


class CreateLog:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)


        return response

    def process_response(self, response):
        print(response.status_code)






