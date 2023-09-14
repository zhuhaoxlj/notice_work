from decouple import config
import json


cookies = json.loads(config('COOKIES_FROM_BROWSER'))
print(cookies)