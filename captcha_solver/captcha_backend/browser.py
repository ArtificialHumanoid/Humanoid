import tempfile
import webbrowser
import time
import os


from captcha_solver.captcha_backend.base import CaptchaBackend


class BrowserBackend(CaptchaBackend):
    def get_submit_captcha_request_data(self, data):
        fd, path = tempfile.mkstemp()
        with open(path, 'w') as out:
            out.write(data)
        url = 'file://' + path
        return {'url': url, 'post_data': None}

    def parse_submit_captcha_response(self, res):
        return res.url.replace('file://', '')

    def get_check_solution_request_data(self, captcha_id):
        url = 'file://' + captcha_id
        return {'url': url, 'post_data': None}

    def parse_check_solution_response(self, res):
        webbrowser.open(url=res.url)
        # Wait some time, skip some debug messages
        # which browser could dump to console
        time.sleep(0.5)
        solution = raw_input('Enter solution: ')
        path = res.url.replace('file://', '')
        os.unlink(path)
        return solution
