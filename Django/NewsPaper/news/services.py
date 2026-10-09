from django.http import HttpRequest

requests_stack = []

class RequestsService:
    @staticmethod
    def peek() -> HttpRequest | None:
        if not len(requests_stack) == 0:
            return requests_stack[-1]
        else:
            return None

    @staticmethod
    def pop() -> HttpRequest | None:
        if not len(requests_stack) == 0:
            return requests_stack.pop()
        else:
            return None

    @staticmethod
    def push(item: HttpRequest):
        if len(requests_stack) == 5:
            requests_stack.pop(0)

        requests_stack.append(item)