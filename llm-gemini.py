import requests
import json

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

payload = json.dumps({
  "contents": [
    {
      "parts": 
        {
          "text": "Explain how AI works in a few words"
        }
    
    }
  ]
})
headers = {
  'x-goog-api-key': 'AIzaSyAxVTsqLtkacPtlvvRyFdP_UREMhkpa5r4',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)