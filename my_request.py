import requests
from requests.exceptions import HTTPError
import urllib3


def get_request(url: str, param: dict, cook={},
                print_resp=False, print_param=True) -> str:
    return my_request(url, param, cook, 'get', print_resp, print_param)


def post_request(url: str, param: dict, cook={},
                print_resp=False, print_param=True) -> str:
    return my_request(url, param, cook, 'post', print_resp, print_param)


def my_request(url: str, param: dict, cook: dict, method: str,
                print_resp: bool, print_param: bool) -> str:
    if method != 'get' and method != 'post':
        print('method is not recognized')
        exit(1)
    if print_param:
        print(*[n[0]+'='+n[1] for n in sorted(param.items())])
    try:
        response = (requests.get(url, params=param, cookies=cook)
                    if method == 'get' else
                    requests.post(url, data=param, cookies=cook))
        if print_resp:
            if method == 'get':
                print(response.url)
            print(response.text)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        if 'SSLCertVerificationError' in str(err):
            response = my_request_not_verify(url, param, cook, method)
            return response.text
        else:
            print(f'Other error occurred: {err}')
            exit(1)
    else:
        return response.text


def my_request_not_verify(url: str, param: dict, cook: dict, method: str) -> str:
    urllib3.disable_warnings()
    try:
        response = (requests.get(url, params=param, cookies=cook, verify=False)
                    if method == 'get' else
                    requests.post(url, data=param, cookies=cook, verify=False))
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        exit(1)
    except Exception as err:
        print(f'Other error occurred: {err}')
        exit(1)
    else:
        return response