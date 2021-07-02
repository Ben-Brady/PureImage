from Classes import Reposts

import os
import sys
from urllib.parse import urlparse
import tqdm
import random
import requests
from dotenv import load_dotenv
load_dotenv()

AuthHeader = {"Authorization": os.environ['PEXEL']}
DB = './Test/Section.db'

os.remove(DB)
Reposts.Setup(DB)
Section = Reposts.Section(0)

JSON = []
for x in range(100):
    r = requests.get(
        url="https://api.pexels.com/v1/search",
        params={
            "query": "leaf",
            "size": "medium",
            "page": x,
            "per_page": 50},
        headers=AuthHeader
    )
    try:
        JSON += r.json()['photos']
    except:
        print(r.text)
        break

IMGs = []
for x in tqdm.tqdm(JSON):
    URL = x['src']['tiny']
    RAW = requests.get(URL).content
    IMGs.append(RAW)
    Filename = (os.path.basename(urlparse(URL).path))
    with open(f"./Test/Images/mass/{Filename}", 'wb') as fObj:
        fObj.write(RAW)


for x in IMGs:
    Section.Add(random.randint(0, 1000000), x)

URL = random.choice(JSON)
IMG = requests.get(URL['src']['tiny'])

Section.Check(IMG.content)
