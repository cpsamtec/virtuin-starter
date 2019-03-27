import requests 

apiPort = os.getenv('
#Send a message to let operator now everything has started successfully 
r = requests.post('http://httpbin.org/post', json={"key": "value"})
