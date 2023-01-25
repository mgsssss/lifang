import requests

endpoint = "http://127.0.0.1:8000/api/product/"

data = {
    "counsel": 180
    , "sequence": 6
    , "heart_rate": 95
    , "emotion_value": "hap"
    , "file_path": "/mkseo/mjy/111"
}
get_response = requests.get(endpoint)
print(get_response.json())