import requests


url = "http://localhost:5000/color"

# Example 1: Request a random color with transparency
response = requests.post(url, json={
    "color": "random",
    "transparency": 80
})
print("Random with transparency:", response.json())

# Example 2: Request a preset color
response = requests.post(url, json={
    "color": "pink"
})
print("Preset color:", response.json())

# Example 3: Request random_preset (random from predefined list)
response = requests.post(url, json={
    "color": "random_preset"
})
print("Random preset:", response.json())

# Example 4: Invalid color
response = requests.post(url, json={
    "color": "beige"
})
print("Invalid color:", response.json())
