import requests

open("test.xlsx",
     "wb").write(requests.get("https://twitter.com/FabrizioRomano/status/1680686166645911557").content)
