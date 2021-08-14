

import requests
first = {
  "name": "first",
  "parent_key": 0,
  "details": "string",
  "timeout_min": 0,
  "timeout_color": "green"
}
second = {
  "name": "second",
  "parent_key": 1,
  "details": "string",
  "timeout_min": 0,
  "timeout_color": "green"
}
third = {
  "name": "third",
  "parent_key": 2,
  "details": "string",
  "timeout_min": 0,
  "timeout_color": "green"
}


result = requests.post("http://127.0.0.1:8000/components/1/config",json=first)
print(result.json())
result = requests.post("http://127.0.0.1:8000/components/2/config",json=second)
print(result.json())

result = requests.post("http://127.0.0.1:8000/components/3/config",json=third)
print(result.json())
