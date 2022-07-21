from analyzer import vid2dict
from numpy import uint8
import json

data = vid2dict("clips/trimmed.mov")

with open("data.json", "w") as f:
    json.dump(data, f, default = lambda o: int(o) if isinstance(o,uint8) else o)