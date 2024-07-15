import requests 

out = requests.get('http://127.0.0.1:8000/camera')
print(out.text)
