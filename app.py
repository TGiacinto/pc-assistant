import os

import pyfiglet
from dotenv import load_dotenv
from termcolor import colored

from ai.chat_gpt import ChatGpt

load_dotenv()


def print_ascii_art():
    return pyfiglet.figlet_format("Pc Assistant")


if __name__ == "__main__":
    art = print_ascii_art()
    colored_art = colored(art, 'blue')
    print(colored_art)

    openai_key = os.getenv("OPENAI_API_KEY", None)
    if openai_key is None:
        openai_key = input("Please enter your OpenAI API key: ")

    ai = ChatGpt(openai_api_key=openai_key)
    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            print("Uscita dal programma.")
            break

        if user_input.lower() == "reset":
            ai.initialize()
            print("Chat resettata")
            continue

        result = ai.run_conversation(text=user_input)
        answer = colored(result.choices[0].message.content, 'green')
        print(answer)
        print()
