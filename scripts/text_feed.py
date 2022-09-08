import requests
import pandas as pd

URL = "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGWjVGWlN4Yk5TY25WUl9iRU1XMjNWY2dUUTJQdzU0WUZObWhDb0RhcmRJVnZBZm1VU1JXQ1NTeDRCZ3ZuMmx4NmxwYzZqczhOTFBySTZWbTBONUNTQXBvaFhjRXZQQzRqN0dkaWVjSGFJMTIxNE09"
response = requests.get(URL)
df = pd.DataFrame(pd.read_excel(response.content))
