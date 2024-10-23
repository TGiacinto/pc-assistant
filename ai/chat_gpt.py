import locale
import platform

import pycountry
from openai import OpenAI

from functions.function_execute import execute_script
from utils.utils import *


class ChatGpt:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = "gpt-4o"
        lang, _ = locale.getdefaultlocale()
        iso639_lang = lang.split('_')[0]
        language_name = pycountry.languages.get(alpha_2=iso639_lang).name
        self.prompt = fetch_prompt('main_prompt.txt')
        info_os = f"{os.name} {platform.system()} {platform.release()}"
        self.prompt = self.prompt.replace("{os}", info_os).replace("{lang}", language_name)
        self.prompt_final_answer = fetch_prompt('answer_prompt.txt').replace("{lang}", language_name)
        self.messages = self.initialize()

    def initialize(self):
        self.messages = []
        return [
            {"role": "system", "content": self.prompt}
        ]

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def run_conversation(self, text):

        self.add_user_message(message=text)

        functions = fetch_function(file_name='functions.json')

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=functions,
            tool_choice="auto",
        )
        response_message = response.choices[0].message

        tool_calls = response_message.tool_calls
        self.messages.append(response_message)
        if tool_calls:
            available_functions = {
                "execute_script": execute_script,
            }
            # extend conversation with assistant's reply
            result_functions = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                result_functions.append(function_response)
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt_final_answer},
                    {"role": "user", "content": "\n".join(result_functions)}
                ],
            )  # get a new response from the model where it can see the function response
            return second_response
        else:
            return response
