import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os

#fetching data from API without authentication

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)
data = response.json()
print("Status Code:", response.status_code)

#print one user's data
print("User Data:", data[0])

#load into pandas dataframe
df_users = pd.DataFrame(data)
print(df_users.head(2))

#extract nested fields

df_users['city']= df_users['address'].apply(lambda x: x['city'])
df_users['company_name'] = df_users['company'].apply(lambda x: x['name'])

print(df_users[['id', 'name', 'username', 'email', 'city', 'company_name']].head(10))

#JSON data from users API
data_1 = [{
    "id": 1,
    "name": "John Kamau",
    "age": 28,
    "email": "john@example.com",
    "city": "Nairobi",
    "occupation": "Data Scientist",
    "is_employed": True,
    "skills": ["Python", "PostgreSQL", "Pandas"]
},
{
    "id": 1,
    "name": "Pascal Opar",
    "age": 32,
    "email": "pascal56@example.com",
    "city": "Nairobi",
    "occupation": "Data Analyst",
    "skills": ["Python", "PostgreSQL", "Pandas"],
    "is_employed": True
}]

#load JSON data into pandas dataframe
df_json = pd.DataFrame(data_1)
print(df_json.head(10))

#using json normalize to flatten nested JSON data
from pandas import json_normalize
df_normalized = json_normalize(data_1)
print(df_normalized.head(2))

#select and rename columns
df_cleaned = df_normalized[['id', 'name', 'age', 'email', 'city', 'occupation', 'is_employed']]
df_cleaned.rename(columns={'id': 'user_id', 'name': 'full_name'}, inplace=True)
print(df_cleaned.head(10))

#load posts into panda as dataframe

url_posts = "https://jsonplaceholder.typicode.com/posts"
response_posts = requests.get(url_posts)   
data_posts = response_posts.json()
df_posts = pd.DataFrame(data_posts)
print(df_posts.head(10)) 

#put vs patch request, for example, updating a user's email address
new_post_data = {
    "userID": 1,
    "title": "Updated Post Title",
    "body": "This is the updated content of the post."}

response = requests.post(url_posts, json=new_post_data)
print("Status Code:", response.status_code)
print("Response Data:", response.json())

#now lets try put- put is used to update the entire resource, while patch is used to update a part of the resource. For example, if we want to update only the title of a post, we can use patch.
update_post_data = {
    "userID": 1,
    "title": "Updated Post Title",
    "body": "This is the updated content of the post."
}

url_put = "https://jsonplaceholder.typicode.com/posts/1"
response_put = requests.put(url_put, json=update_post_data)
print("PUT Status Code:", response_put.status_code)
print("PUT Response Data:", response_put.json())

#patch request is used to update a part of the resource. For example, if we want to update only the title of a post, we can use patch.
update_post_data_patch = {
    "title": "Patched Post Title"
}
url_patch = "https://jsonplaceholder.typicode.com/posts/1"
response_patch = requests.patch(url_patch, json=update_post_data_patch)
print("PATCH Status Code:", response_patch.status_code)
print("PATCH Response Data:", response_patch.json())

#DELETE request is used to delete a resource. For example, if we want to delete a post, we can use delete.
url_delete = "https://jsonplaceholder.typicode.com/posts/1"
response_delete = requests.delete(url_delete)
print("DELETE Status Code:", response_delete.status_code)
print("DELETE Response Data:", response_delete.json())

if response_delete.status_code == 200:
    print("Post deleted successfully.")

#working with apis with keys or api key and json

city = "Nairobi"
load_dotenv()
api_key = os.getenv("api_key")

api_url ="https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key + "&units=metric"

response = requests.get(api_url)
data = response.json()
print("Status Code:", response.status_code)
print("Response Data:", json.dumps(data, indent=4))


df_weather = pd.json_normalize(data)
print(df_weather.head(10))

#select uuseful colums

df_weather_cleaned = df_weather[['name', 'main.temp', 'main.humidity', 'weather', 'wind.speed', 'sys.country']]

df_weather['condition']= df_weather['weather'].apply(lambda x: x[0]['description'])  
df_weather=df_weather.rename(columns={'name': 'city', 'main.temp': 'temperature', 'main.humidity': 'humidity', 'wind.speed': 'wind_speed', 'sys.country': 'country'})   
print(df_weather_cleaned.head(10))

#calculate average temperature and humidity for multiple cities, for example, Nairobi, Mombasa, Kisumu
cities = ["Nairobi", "Mombasa", "Kisumu"]
df_weather['date']=pd.to_datetime(df_weather['dt']).dt.time
avg_temp = df_weather.groupby('date')['temperature'].mean().reset_index()
avg_humidity = df_weather.groupby('date')['humidity'].mean().reset_index()
print(avg_temp.head(10))
print(avg_humidity.head(10))

#most common weather condition for each city
most_common_condition = df_weather.groupby('city')['condition'].agg(lambda x: x.mode()[0]).reset_index()
print(most_common_condition.head(10))

#calculate max humindity and temperature for each city
max_temp_humidity = df_weather.groupby('city')[['temperature', 'humidity']].max().reset_index()
print(max_temp_humidity.head(10))

#how to bring multiple cities data into one dataframe, for example, Nairobi, Mombasa, Kisumu
cities = ["Nairobi", "Mombasa", "Kisumu", "Kisii", "Eldoret"]
records = []

for city in cities:
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(api_url)
    data = response.json()
    records.append({
        "city": data.get("name"),
        "temperature": data.get("main", {}).get("temp"),
        "humidity": data.get("main", {}).get("humidity"),
        "condition": data.get("weather", [{}])[0].get("description"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "country": data.get("sys", {}).get("country")
   })
print("Status Code:", response.status_code)
print("Response Data:", json.dumps(data, indent=4))
print("Printing records for multiple cities:")
print(records)

#convert records to pandas dataframe
df_multiple_cities = pd.DataFrame(records)
print(df_multiple_cities.head(5))

#file handing excel




