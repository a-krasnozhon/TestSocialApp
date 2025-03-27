from core import execute_request
from response import Response


if __name__ == '__main__':
    while True:
        try:
            response = execute_request(input('> '))
            if isinstance(response, Response):
                if response.content:
                    print(response)
            else:
                print(f'{response} is not Response class instance')
        except ValueError as e:
            print(e)
