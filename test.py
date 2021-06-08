import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "referer": "http://www.google.com"
}
parameters = {
    'district_id' : "540",
    "date" : "08-06-2021",
}
response = requests.get(
    #"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict", 
    #headers=headers, params=parameters
    "http://cdn-api.co-vin.in/api/v2/admin/location/states", headers=headers
)

print(response.status_code)
