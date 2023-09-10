import flet as ft
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):

    # def route_change(e: ft.RouteChangeEvent):
    #     page.add(ft.Text(f"New route: {e.route}"))

    def go_chat(e):
        print('elko', join_user_name.value)
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.clean()
            page.session.set("user_name", join_user_name.value)
            page.update()

        page.route = "/chat"

        def on_message(message: Message):
            if message.message_type == "chat_message":
                m = ChatMessage(message)
            elif message.message_type == "login_message":
                m = ft.Text(message.text, italic=True,
                            color=ft.colors.BLACK45, size=12)
            chat.controls.append(m)
            page.update()

        page.pubsub.subscribe(on_message)

        # Chat messages
        chat = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

        def chatgpt_old(message):
            import openai

            # Set up the OpenAI API client
            openai.api_key = os.getenv("OPENAI_APIKEY")

            # Set up the model and prompt
            model_engine = "text-davinci-003"
            prompt = message
            # Generate a response
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )

            response = completion.choices[0].text.strip()
            if response.startswith('\n'):
                response = response[1:]
            return response

        def chatgpt(message):

            # import openai
            from langchain.llms import OpenAI
            from langchain.chat_models import ChatOpenAI
            from langchain import PromptTemplate
            from langchain.chains import LLMChain
            from langchain.prompts.chat import (
                ChatPromptTemplate,
                SystemMessagePromptTemplate,
                HumanMessagePromptTemplate,
            )

            # Set up the OpenAI API client
            openai_api_key = os.getenv("OPENAI_APIKEY")

            chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

            # Template to use for the system message prompt
            template = f"""
                You are a scary ghost and you want to scare people. You are talking to {join_user_name.value}. 
                Ask him/her different creepy questions. If they answer only with yes or no ask them for more information to keep
                conversion going. Do not repeat same question all over agagin.
                """

            system_message_prompt = SystemMessagePromptTemplate.from_template(template)

            # Human question prompt
            human_template = "Answer to that message based on whole conversation: {message}"
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)


            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, message]
            )

            chain = LLMChain(llm=chat, prompt=chat_prompt)

            response = chain.run(question=message)
            response = response.replace("\n", "")
            return response

        def send_message_click(e):
            print('ALERtTT', new_message.value)
            if new_message.value != "":
                page.pubsub.send_all(Message(page.session.get(
                    "user_name"), new_message.value, message_type="chat_message"))
                temp = new_message.value
                new_message.value = ""
                new_message.focus()
                res = chatgpt(temp)
                print('ALERtTT-res', res)
                if len(res) > 220:  # adjust the maximum length as needed
                    res = '\n'.join([res[i:i+220]
                                    for i in range(0, len(res), 220)])
                page.pubsub.send_all(
                    Message("ChatGPT", res, message_type="chat_message"))
                page.update()

        # A new message entry form
        new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=send_message_click,
        )

        # Add everything to the page
        page.add(
            ft.Container(
                content=chat,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    new_message,
                    ft.IconButton(
                        icon=ft.icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=send_message_click,
                    ),
                ]
            ),
        )

        page.update()

    # page.on_route_change = route_change
    join_user_name = ft.TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=go_chat)
    page.add(
        join_user_name
        # ft.ElevatedButton("Submit", on_click=go_chat)
    )

import logging
logging.basicConfig(level=logging.DEBUG)

# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main)