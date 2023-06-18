import requests
import json

s = requests.Session()

# URL of your Flask application
url = 'http://localhost:5000/chat'
questions = ['hi, can you help me with some math?', '1+1=?', '3*5=?']
# while True:
# Get user input
user_input = input('User: ')

# Send POST request to your Flask application
response = s.post(url, json={'input': user_input})

# Print the response from the ChatGPT model
print("AI: ", json.loads(response.text))
