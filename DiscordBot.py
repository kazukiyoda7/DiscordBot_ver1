import openai
import discord
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
TOKEN = os.getenv('TOKEN')

openai.api_key = API_KEY

class ChatGPT:
    def __init__(self, system_setting):
        self.system = {"role": "system", "content": system_setting}
        self.input_list = [self.system]
        self.logs = []

    def input_message(self, input_text):
        self.input_list.append({"role": "user", "content": input_text})
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.input_list
        )
        self.logs.append(result)
        self.input_list.append(
            {"role": "assistant", "content": result.choices[0].message.content}
        )


intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("起動完了")

# メッセージが送信されたときに呼び出されるイベントハンドラ
@client.event
async def on_message(message):
    # メッセージを送信したユーザーがBot自身である場合は無視する
    if message.author == client.user:
        return

    # Botに「!q [質問]」という形式で質問された場合
    if message.content.startswith('!gpt'):
        # 質問を取得する
        question = message.content[4:]

        # GPT APIを使用して回答を生成する
        api = ChatGPT(system_setting="あなたはアシスタントです。では、会話を開始します。")
        api.input_message(question)

        # 回答を取得する
        answer = api.input_list[-1]["content"]

        # 回答を送信する
        await message.channel.send(answer)

# Discord Botを起動する
client.run(TOKEN)