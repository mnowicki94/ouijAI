import flet as ft
from dotenv import load_dotenv
import os
import openai
import textwrap
import random

from chatbot import chatgpt
from features import txt2speech, generate_face, local_image

load_dotenv()  # take environment variables from .env.

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


    chat_id = int(random.random() * 10000000000000000)


    audio1 = ft.Audio(
        # src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
        src='./content/ambient_c_motion.mp3',
        autoplay=True)

    page.overlay.append(audio1)


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
        chat_gpt = chatgpt(user = join_user_name.value, age = join_user_age.value, desc = join_user_desc.value, scare = join_user_scare.value)


        #LOADING SCREEN

        # these two lines will align the text center in the app
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        page.add(
            ft.Image(
                src='./content/ouija2.jpeg',
                # src="./content/ouija.gif",
                fit=ft.ImageFit.COVER,
                expand=True,
            )
        )


        page.add(ft.Text("Searching for ghosts...",
                 size=32,  # Increasing the size of the text
                 weight=ft.FontWeight.BOLD  # it will bold the text
                 ))

        page.splash = ft.ProgressBar()


        page.update()


        # GENERATE FACE
        img_path = generate_face()
        # img_path = local_image()

        img = ft.Image(
            src_base64=img_path,
            width=500,
            height=500,
            fit=ft.ImageFit.CONTAIN,
        )

        page.splash = None

        #ugly solution to improve in future
        del page.controls[1], page.controls[0]

        page.update()


        page.add(img)
        page.update()

        def send_message_click(e):
            print('ALERtTT', new_message.value)
            if new_message.value != "":

                page.pubsub.send_all(Message(page.session.get(
                    "user_name"), new_message.value, message_type="chat_message"))
                temp = new_message.value
                new_message.value = ""
                new_message.focus()
                res = chat_gpt.ChatGptResponse(temp, id=chat_id)
                xres = res
               
                # Wrap this text.
                wrapper = textwrap.TextWrapper(width=50) 
                string = wrapper.fill(text=res)
                # if len(res) > 220:  # adjust the maximum length as needed
                #     res = '\n'.join([res[i:i+220]
                #                     for i in range(0, len(res), 220)])
                page.pubsub.send_all(
                    Message("Negative 00 Ghost 27", string, message_type="chat_message"))

                #READ ANSWER
                txt2speech(xres)


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

    join_user_age = ft.TextField(
        label="Enter your Age",
        autofocus=True,
        on_submit=go_chat)

    join_user_desc = ft.TextField(
        label="Write something about yourself",
        autofocus=True,
        on_submit=go_chat)

    join_user_scare = ft.TextField(
        label="Write what are you afraid of",
        autofocus=True,
        on_submit=go_chat)

    page.add(
        join_user_name,
        join_user_age,
        join_user_desc,
        join_user_scare,
        # ft.ElevatedButton("Submit", on_click=go_chat)
    )


import logging
logging.basicConfig(level=logging.DEBUG)

# ft.app(target=main, view=ft.AppView.WEB_BROWSER,  port=8080)

ft.app(target=main)