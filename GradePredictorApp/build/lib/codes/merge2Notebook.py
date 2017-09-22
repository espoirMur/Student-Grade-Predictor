import json
import os

folder = "slides"
prefix = "quiz"
paths = [os.path.join(folder, name) for name in os.listdir(folder) if name.startswith(prefix) and name.endswith(".ipynb")]
result = json.loads(open(paths.pop(0), "r").read())
for path in paths:
    result["worksheets"][0]["cells"].extend(json.loads(open(path, "r").read())["worksheets"][0]["cells"])
open(os.path.join(folder, "compil_%s.ipynb" % prefix), "w").write(json.dumps(result, indent = 1))