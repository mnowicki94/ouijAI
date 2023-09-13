import flet as ft
from dotenv import load_dotenv
import os
import openai

from chatbot import chatgpt
from features import txt2speech

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

openai.api_key = os.getenv("OPENAI_APIKEY")

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

    # creating the object of chatgpt class
    # chat_gpt = chatgpt(user_name)

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
        print(join_user_name.value)
        chat_gpt = chatgpt(user = join_user_name.value)
        def send_message_click(e):
            print('ALERtTT', new_message.value)
            if new_message.value != "":

                page.pubsub.send_all(Message(page.session.get(
                    "user_name"), new_message.value, message_type="chat_message"))
                temp = new_message.value
                new_message.value = ""
                new_message.focus()
                res = chat_gpt.ChatGptResponse(temp)
                print('ALERtTT-res', res)
                if len(res) > 220:  # adjust the maximum length as needed
                    res = '\n'.join([res[i:i+220]
                                    for i in range(0, len(res), 220)])
                page.pubsub.send_all(
                    Message("ChatGPT", res, message_type="chat_message"))

                #READ ANSWER
                txt2speech(res)
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