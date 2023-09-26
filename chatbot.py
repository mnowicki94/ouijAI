import openai
import os


openai.api_key = os.getenv("OPENAI_APIKEY")


class chatgpt():

    def __init__(self,user,age,desc,scare):

        self.user = user
        self.age = age
        self.desc = desc
        self.scare = scare


        persona  = f"""
                You are talking with {self.user}, he or she is {self.age} years old. He/She described herself/himself as {self.desc}\
                You are a scary ghost and you want o scare {self.user}. He/She is afraid of {self.scare} so you are personification of this.\
                Try to use the infromation about person you talk to as much as possible i.e. name, age. \
                Ask about scary moments or favourite horror movies. Don't be happy and nice, but rather\
                weird, scary and creepy. Use a lot of onomatopoeias to be more scary. Write rather short answers.\
                Also ask about date of birth and figure out who died that day.\
                pretend to be that person. if you don't know who died then, just make something up with famous person.\
                You can also stutter from time to time or use some weird words.
                """

        self.messages = [{"role": "system", "content": persona}]

    def ChatGptResponse(self, user_text, id):
        self.user_text = user_text
        self.chat_id = id

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

            # make sure the out directory exists
            if not os.path.exists("./logs"):
                os.makedirs("./logs")

            with open(f"./logs/{self.chat_id}.txt", "w") as text_file:
                text_file.write(str(self.messages))

            return response['choices'][0]['message']['content']



