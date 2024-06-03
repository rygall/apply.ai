import requests

def call_api():
    url = "https://api.screenshotone.com/take?access_key=dI4hFlJDD9hyaQ&url=https%3A%2F%2Fcareers.leidos.com%2Fjobs%2F14319040-machine-learning-research-scientist&full_page=true&full_page_scroll=false&viewport_width=1920&viewport_height=1080&device_scale_factor=1&format=jpg&image_quality=80&block_ads=true&block_cookie_banners=true&block_banners_by_heuristics=false&block_trackers=true&delay=0&timeout=60"
    params = None
    method = "GET"
    headers = None
    data = None
    response = requests.request(method, url, headers=headers, params=params, data=data)
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}")