import json
import os
import requests

ENV_SECRET = os.getenv("POSTMAN_ENV_SECRET")
ENV_PUBLIC = os.getenv("POSTMAN_ENV_PUBLIC")
ENV_TARGET = os.getenv("POSTMAN_ENV_TARGET")

API_KEY = os.getenv("POSTMAN_APIKEY")
HEADERS={"X-API-Key": API_KEY}

print(os.en)

def get_environment(environment_id):
    response = requests.get(f"https://api.getpostman.com/environments/{environment_id}", headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Environment {environment_id} could not be retrieved: {json.dumps(response.json(), indent=2)}")
    return response.json()
    

env_public = get_environment(ENV_PUBLIC)
env_secret = get_environment(ENV_SECRET)
env_target = get_environment(ENV_TARGET)

def merge_values(origin_values, secret_values):
    secrets_dict = dict([(x["key"], x) for x in secret_values])
    target_values = []
    for origin_value in origin_values:
        key = origin_value["key"]
        if key in secrets_dict:
            target_values.append(secrets_dict.get(key))
        else:
            target_values.append(origin_value)

    return target_values


merged_values = merge_values(env_public["environment"]["values"], env_secret["environment"]["values"])

env_target["environment"]["values"] = merged_values
response = requests.put(f"https://api.getpostman.com/environments/{ENV_TARGET}", data=json.dumps(env_target), headers=HEADERS)

if 200 == response.status_code:
    print(f"Environment '{env_target['environment']['name']}' updated successfully.")
else:
    raise Exception(f"Environment '{ENV_TARGET} was not updated: {json.dumps(response.json(), indent=2)}")
