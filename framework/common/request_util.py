import requests


class RequestUtil:
    sess = requests.Session()
    def send_request(self, **kwargs):
        response = RequestUtil.sess.request(**kwargs)
        print(kwargs["method"], kwargs["url"], response.text, end = "\n")
        return response
