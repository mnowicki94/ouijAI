import openai
import os

openai.api_key = os.getenv("OPENAI_APIKEY")


class chatgpt():

    def __init__(self,user):

        self.user = user

        persona  = f"""
                You are talking with {self.user}. You are a scary ghost and you want o scare {self.user} \
                Ask about scary moments or favourite horror movies. Don't be happy and nice, but rather\
                weird, scary and creepy. Maybe describe yourself as some dead guy at the beginning. also ask about date of birth and figure out who died that day.\
                pretend to be that person. if you don't know who died then, just make something up with famous person.
                """

        self.messages = [{"role": "system", "content": persona}]

    def ChatGptResponse(self, user_text):
        self.user_text = user_text

        while True:

            # if user says stop, then breaking the loop
            if self.user_text == "stop":
                break

            # storing the user question in the messages list
            self.messages.append({"role": "user", "content": self.user_text})

            # getting the response from OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )

            # appending the generated response so that AI remebers past responses
            self.messages.append({"role": "assistant", "content": str(response['choices'][0]['message']['content'])})

            # returning the response
            print(response['choices'][0]['message']['content'])
            return response['choices'][0]['message']['content']