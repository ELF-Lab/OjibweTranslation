# this code section initialize a LLM model through API call to Grog
import json
from groq import Groq
import time

def hello(name):
    return f"Hello {name}. 42"

def get_api_key(filename="../env/credentials.json"):
    # load api key
    api_key = ""
    with open(filename) as f:
        login = json.load(f)
        
        api_key = login["GROQ_API_KEY"]
    
    return api_key

def connect(api_key):
    try:
        # put your api key here, or in "./data/credentials.json"
        client = Groq(api_key=api_key)
        print("Connection OK")
    except:
        print("Error connecting to Groq")
        return None
    return client

def send_request(prompt, client, sleep_time=1):
    result = ""
    try:
        completion = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1,
                    max_tokens=200,
                    stream=False,
                    response_format={"type": "json_object"},
                    stop=None,
                )
    
        result = completion.choices[0].message.content
            
    except Exception as err:
        print("Skipping, error =", err)
        result = ""
        

     # pause to avoid hitting bandwidth limit (~ 14K token / minute)
    print(f"Pausing for {sleep_time} secs...", end="")
    time.sleep(sleep_time)
    print("OK")
    
    return result
