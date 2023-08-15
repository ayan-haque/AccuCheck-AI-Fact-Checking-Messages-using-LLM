import os
import pandas as pd
import json
from tqdm import tqdm
import openai

openai.api_key = os.environ.get('PRIVATE_KEY')

class checkMessage:
    
    def __init__(self):
        pass
    
    def convert_sub_objects_to_dict(self, obj):
        if isinstance(obj, list):
            return [self.convert_sub_objects_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.convert_sub_objects_to_dict(value) for key, value in obj.items()}
        elif hasattr(obj, 'json'):
            return json.loads(obj.json())
        else:
            return obj
        
    
    def callChatGPT(self, input_text):
        
        #input_prompt = "I have receive the message following message: " + '"' + str(input_text)  + '"'  + "."
        input_prompt = "I have receive the following forwared message of whatsapp which I have enclosed within triple backsticks " + '```' + str(input_text)  + '```'  + "."
        
        #input_prompt = input_prompt + " \n Can you check if the message is factually correct? \n Please give numerical point wise answer for long messages and do not repeat the original message in your response. \n Keep your response on points concise. \n Make sure you're giving fact check results and nothing else"
        input_prompt = input_prompt + " \nNow, Can you please check if the message is factually correct?. \nImportant note: Always consider the following points while giving your response: \n 1) Always give numerical point wise answer for long messages \n 2) Never repeat the original message in your response. \n 3) Keep your response on point and concise. \n 4) Make sure you're giving fact check results and nothing else. \n 5) Finally based on your fact check, If the message contains all correct facts then give this exact message at the end: " + '"' + 'All facts are correct! The message can be forwarded' + '"' + '.' + ' Else incase the message contains factually incorrect information, then give this exact message in the end: '  + '"' + "WARNING: Please do not forward this message, as it contains incorrect information!" + '"' + "." + "\nPlease take your time and do not rush for results." 
        
        input_prompt = str(input_prompt)
        print("Input prompt is: ", input_prompt)

        response_chatGPT_json = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "user", "content": input_prompt}
            ]
        )
        
        response_chatGPT_json = self.convert_sub_objects_to_dict(response_chatGPT_json)
        response_chatGPT = response_chatGPT_json["choices"][0]["message"]["content"]
        
        return response_chatGPT


'''
# Testing
input_text = "Donald Trump was one of the president of United states"
checkMessage_obj = checkMessage()
response_AI = checkMessage_obj.callChatGPT(input_text)
'''

