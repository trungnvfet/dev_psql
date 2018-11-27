from oslo_config import cfg
from urllib.request import urlopen
import json
from db import *

CONF = cfg.CONF

if __name__ == '__main__':
    response = urlopen("https://api.github.com/users?since=100")
    html = response.read()
    d = json.loads(html.decode())
    register_opts(CONF)
    create_tables()
