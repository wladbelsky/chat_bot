import json
import random
from aiogram import Router
from aiogram.types import Message
from openai import AsyncOpenAI
from config import CHAT_GPT_TOKEN, MEMORY_TIME, OPERATOR_LIST
from database.redis_db import Redis

router = Router()
client = AsyncOpenAI(api_key=CHAT_GPT_TOKEN)


tools = [
    {
        "type": "function",
        "function": {
            "name": "switch_to_operator",
            "description": "Переключиться на живого оператора",
        }
    }
]


@router.message()
async def gpt(message: Message):
    redis = Redis()
    user_id = message.from_user.id
    async with redis.get_connection() as connection:
        async with connection.pipeline() as pipe:
            if user_id in OPERATOR_LIST:
                connected_user_id = (await (pipe.get(f"operator:{user_id}_user_id").execute()))[0]
                if connected_user_id:
                    await message.bot.send_message(connected_user_id, message.text)
                    await message.answer("Сообщение отправлено пользователю")
                else:
                    await message.answer("Нет подключенных пользователей")
                return
            state = (await (pipe.get(f"user:{user_id}_state").execute()))[0]
            if not state:
                state = "default"
            if state == "default":
                context_str = (await (pipe.get(f"user:{user_id}_context").execute()))[0]
                if context_str:
                    context: list = json.loads(context_str)
                else:
                    context = [
                        {
                            "role": "system",
                            "content": "Ты сотрудник техподдержки, вежливо отвечай на вопросы пользователей, помогай им решать проблемы. Если пользователь попросит переключиться на живого оператора, то ты должен это сделать."
                        }
                    ]
                context.append({
                    "role": "user",
                    "content": message.text
                })
                context_str = json.dumps(context)
                pipe = pipe.set(f"user:{user_id}_context", context_str, ex=MEMORY_TIME)
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=context,
                    tools=tools
                )
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls
                if tool_calls:
                    for tool_call in tool_calls:
                        if tool_call.function.name == "switch_to_operator":
                            pipe = pipe.set(f"user:{user_id}_state", "operator", ex=MEMORY_TIME)
                            operator_id = random.choice(OPERATOR_LIST)
                            pipe = pipe.set(f"user:{user_id}_operator_id", operator_id, ex=MEMORY_TIME)
                            pipe = pipe.set(f"operator:{operator_id}_user_id", user_id, ex=MEMORY_TIME)
                            #  Берем случайного оператора из списка
                            #  но по нормальному бы сделать выбор оператора по его загруженности
                            await message.answer("Переключаю на человека")
                            await message.bot.send_message(operator_id, f"Пользователь {message.from_user.username} хочет поговорить с вами")
                            await pipe.execute()
                            return
                await message.answer(response_message.content)
            elif state == "operator":
                pipe = pipe.set(f"user:{user_id}_state", "operator", ex=MEMORY_TIME)
                _, operator_id = (await (pipe.get(f"user:{user_id}_operator_id").execute()))
                pipe = pipe.set(f"user:{user_id}_operator_id", operator_id, ex=MEMORY_TIME)
                await message.bot.send_message(operator_id, message.text)
                await message.answer("Сообщение отправлено оператору")
            await pipe.execute()
