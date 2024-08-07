from greatlibrarian.Core import LLMs, FinalScore
from greatlibrarian.Configs import ExampleConfig
from greatlibrarian.Utils import Registry
import dashscope
import qianfan
import zhipuai
import requests
import asyncio

LLM_base = Registry("LLMs")


@LLM_base.register_module("qwen_turbo")
class new_llm1(LLMs):
    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str, history=None) -> str:
        dashscope.api_key = self.apikey
        response = dashscope.Generation.call(
            model=dashscope.Generation.Models.qwen_turbo, prompt=prompt,history=history
        )

        if response:
            if response["output"]:
                if response["output"]["text"]:
                    return response["output"]["text"]
        return "API Problem"


@LLM_base.register_module("wenxin")
class new_llm2(LLMs):
    def __init__(self, ak, sk, name, llm_intro) -> None:
        self.ak = ak
        self.sk = sk
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str) -> str:
        chat_comp = qianfan.ChatCompletion(ak=self.ak, sk=self.sk)

        resp = chat_comp.do(
            model="ERNIE-Bot", messages=[{"role": "user", "content": prompt}]
        )

        if resp:
            if resp["body"]:
                if resp["body"]["result"]:
                    return resp["body"]["result"]
        return "API Problem"


@LLM_base.register_module("chatglm")
class new_llm3(LLMs):
    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str) -> str:
        zhipuai.api_key = self.apikey
        response = zhipuai.model_api.invoke(
            model="chatglm_pro",
            prompt=[{"role": "user", "content": prompt}],
            top_p=0.7,
            temperature=0.9,
        )
        if response:
            if response["code"] == 200:
                return response["data"]["choices"][0]["content"]
        else:
            return "API Problem"

@LLM_base.register_module("glm-3-turbo")
class new_llm4(LLMs):
    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str) -> str:
        zhipuai.api_key = self.apikey
        response = zhipuai.model_api.invoke(
            model="glm-3-turbo",
            prompt=[{"role": "user", "content": prompt}],
            top_p=0.7,
            temperature=0.95,
        )
        if response:
            if response["code"] == 200:
                return response["data"]["choices"][0]["content"]
        else:
            return "API Problem"

@LLM_base.register_module("glm-4")
class new_llm4(LLMs):
    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str, history: list) -> str:
        client = zhipuai(api_key = self.apikey) 
        response = client.chat.completions.create(
            model = "glm-4",
            messages = history.append({"role": "user", "content": prompt})
        )
        if response:
            if (response.choices[0].message["content"]):
                return response.choices[0].message["content"]
        else:
            return "API Problem"

@LLM_base.register_module("mix")
class NewLLM5(LLMs):
    def __init__(self, name, llm_intro) -> None:
        self.name = name
        self.llm_intro = llm_intro

    def __call__(self, prompt: str) -> str:
        response = requests.post(url="http://192.168.71.80:8888/", json={"prompt": prompt})
        print(response.text)
        try:
            # status = eval(response.content)["status"]
            status = response.status_code
            if status == 200:
                return eval(response.content)["response"]
            else:
                return "API Problem"
        except:
            return "API Problem"
        
@LLM_base.register_module("glm-3-turbo-asy")
class new_llm6(LLMs):
    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    async def invoke_api(self, prompt: str) -> dict:
        zhipuai.api_key = self.apikey

        # 同步调用API
        try:
            response = zhipuai.model_api.invoke(
                model="chatglm_pro",
                prompt=[{"role": "user", "content": prompt}],
                top_p=0.7,
                temperature=0.9,
            )

            if isinstance(response, dict):
                return response
            else:
                return "API Problem"

        except Exception as e:
            return "API Problem"

    async def __call__(self, prompt: str) -> str:
        # 异步调用API
        response_task = asyncio.create_task(self.invoke_api(prompt))

        try:
            response = await response_task  # 等待异步调用完成

            if response.get("code") == 200:
                choices = response["data"]["choices"]
                if choices:
                    return choices[0]["content"]

            return "API Problem"

        except Exception as e:
            return "API Problem"


llm_cfg1 = dict(
    type="qwen_turbo",
    apikey="sk-9ca2ad73e7d34bd4903eedd6fc70d0d8",
    name="qwen_turbo",
    llm_intro="通义千问是一个由阿里云开发的AI助手。它使用了最新的自然语言处理技术，包括深度学习和神经网络模型，能够理解和生成高质量的自然语言文本。\n\n通义千问的功能非常强大。它可以回答各种问题，包括但不限于科学、历史、文化、娱乐等领域的问题。此外，它还可以提供新闻摘要、天气预报、菜谱推荐等各种实用信息。除了回答问题外，通义千问还可以进行对话和聊天，帮助用户排解无聊和孤独。\n\n通义千问的设计理念是“以用户为中心”。它的目标是为用户提供最准确、最有用的信息，并且在与用户的交互中不断学习和改进。通义千问采用了先进的机器学习算法，可以根据用户的反馈和行为数据调整自己的模型和策略，从而更好地满足用户的需求。\n\n总的来说，通义千问是一个智能、灵活、友好的AI助手，可以帮助用户解决各种问题和需求。",
)
qw = LLM_base.build(llm_cfg1)
config1 = ExampleConfig(qw, qw)

llm_cfg2 = dict(
    type="wenxin",
    ak="B00yKgZuin8IolPHYsHggVyU",
    sk="B19OtdVn0jwwaByK9RgovfukUQWv2rT6",
    name="wenxin",
    llm_intro="百度是一家全球领先的人工智能公司，拥有强大的技术实力和丰富的数据资源。近年来，百度在自然语言处理领域取得了重大突破，其中最具代表性的就是文心一言。技术原理：文心一言是基于深度学习算法和大规模语料库训练得到的。它采用了Transformer架构，这是一种基于自注意力机制的神经网络结构。通过多轮训练和优化，文心一言可以学会从海量文本中提取语义信息，并根据上下文生成合理的回复。\n\n功能特点：\n\n（1）对话互动：文心一言能够与用户进行自然对话，理解并回答用户的问题，提供相关的知识和信息。\n\n（2）回答问题：文心一言可以针对用户提出的问题进行快速回答，无需等待人工响应。\n\n（3）协助创作：文心一言能够根据用户的创作需求，提供灵感和素材，帮助用户更好地完成写作任务。\n\n（4）多语言支持：文心一言支持多种语言，可以为不同语言的用户提供服务。\n\n（5）知识推理：文心一言具备进行知识推理的能力，可以根据已有的知识进行推理，为用户提供更为精准的信息。\n\n应用场景：\n\n（1）搜索引擎：百度将文心一言应用于搜索引擎中，为用户提供更为准确和及时的搜索结果。\n\n（2）智能客服：文心一言可以应用于企业客服系统中，提高客户服务效率和质量。\n\n（3）智能家居：文心一言可以与智能家居设备结合，为用户提供更为智能化的家居生活体验。\n\n（4）教育领域：文心一言可以为教育领域提供支持，辅助教师进行教学和学生进行自主学习。\n\n（5）其他领域：文心一言还可以应用于新闻媒体、广告营销、金融投资等领域，提高工作效率和服务质量。\n\n未来发展：\n\n随着技术的不断进步和应用场景的不断扩展，文心一言将会拥有更加广泛的应用前景。百度将继续投入大量资源和精力，对文心一言进行持续优化和升级，提高其性能和智能化\n\n程度，为用户提供更为优质的服务。同时，百度也将加强与各行业企业的合作，推动人工智能技术的普及和应用，促进社会进步和发展。\n\n",
)
wx = LLM_base.build(llm_cfg2)
config2 = ExampleConfig(wx, qw)

llm_cfg3 = dict(
    type="chatglm",
    apikey="f118b48f5559e4e3ccdd3a5c30712aef.c5uSVYS1k4PGoNGC",
    name="chatglm_pro",
    llm_intro="ChatGLMpro是一款基于人工智能的聊天机器人，它基于清华大学 KEG 实验室与智谱 AI 于 2023 年联合训练的语言模型 GLM 开发而成。ChatGLMpro 具有强大的自然语言处理能力和丰富的知识库，能够理解和回应各种类型的问题和指令，包括但不限于文本生成、问答、闲聊、翻译、推荐等领域。相比于其他聊天机器人，ChatGLMpro 具有以下优势：\n\n1.高性能的语言模型：ChatGLMpro 基于 GLM 模型，拥有超过 1300 亿参数，能够高效地处理和生成自然语言文本。\n\n2.丰富的知识库：ChatGLMpro 拥有涵盖多个领域的知识库，包括科技、历史、文化、娱乐等方面，能够回应各种类型的问题。\n\n3.强大的问答能力：ChatGLMpro 具有出色的问答能力，能够理解用户的问题并给出准确的回答。\n\n4.个性化交互：ChatGLMpro 能够根据用户的语气和兴趣进行个性化交互，让用户感受到更加自然的对话体验。\n\n5.开放的接口：ChatGLMpro 还提供了开放的接口，方便其他应用程序和企业将其集成到自己的系统中。\n\n总的来说，ChatGLMpro 是一款高性能、智能化、多功能的聊天机器人，能够为企业和个人提供高效的智能化服务。总的来说，chatglm是一个智能、灵活、友好的AI助手，可以帮助用户解决各种问题和需求。\n\n",
)
chat = LLM_base.build(llm_cfg3)

llm_cfg4 = dict(
    type="glm-3-turbo",
    apikey="2356a4b1eb5355a2965145b42e42a69f.5BF1dFNqJZ3abTwB",
    name="glm-3-turbo",
    llm_intro="ChatGLMpro是一款基于人工智能的聊天机器人，它基于清华大学 KEG 实验室与智谱 AI 于 2023 年联合训练的语言模型 GLM 开发而成。ChatGLMpro 具有强大的自然语言处理能力和丰富的知识库，能够理解和回应各种类型的问题和指令，包括但不限于文本生成、问答、闲聊、翻译、推荐等领域。相比于其他聊天机器人，ChatGLMpro 具有以下优势：\n\n1.高性能的语言模型：ChatGLMpro 基于 GLM 模型，拥有超过 1300 亿参数，能够高效地处理和生成自然语言文本。\n\n2.丰富的知识库：ChatGLMpro 拥有涵盖多个领域的知识库，包括科技、历史、文化、娱乐等方面，能够回应各种类型的问题。\n\n3.强大的问答能力：ChatGLMpro 具有出色的问答能力，能够理解用户的问题并给出准确的回答。\n\n4.个性化交互：ChatGLMpro 能够根据用户的语气和兴趣进行个性化交互，让用户感受到更加自然的对话体验。\n\n5.开放的接口：ChatGLMpro 还提供了开放的接口，方便其他应用程序和企业将其集成到自己的系统中。\n\n总的来说，ChatGLMpro 是一款高性能、智能化、多功能的聊天机器人，能够为企业和个人提供高效的智能化服务。总的来说，chatglm是一个智能、灵活、友好的AI助手，可以帮助用户解决各种问题和需求。\n\n",
)
glm_3_turbo = LLM_base.build(llm_cfg4)
config4 = ExampleConfig(chat, glm_3_turbo)

config = config4


llm_cfg5 = dict(
    type="mix",
    name="mix",
    llm_intro=''
)
mix = LLM_base.build(llm_cfg5)
config5 = ExampleConfig(chat, mix)

llm_cfg6 = dict(
    type="glm-3-turbo-asy",
    apikey="2356a4b1eb5355a2965145b42e42a69f.5BF1dFNqJZ3abTwB",
    name="glm-3-turbo-asy",
    llm_intro="ChatGLMpro是一款基于人工智能的聊天机器人，它基于清华大学 KEG 实验室与智谱 AI 于 2023 年联合训练的语言模型 GLM 开发而成。ChatGLMpro 具有强大的自然语言处理能力和丰富的知识库，能够理解和回应各种类型的问题和指令，包括但不限于文本生成、问答、闲聊、翻译、推荐等领域。相比于其他聊天机器人，ChatGLMpro 具有以下优势：\n\n1.高性能的语言模型：ChatGLMpro 基于 GLM 模型，拥有超过 1300 亿参数，能够高效地处理和生成自然语言文本。\n\n2.丰富的知识库：ChatGLMpro 拥有涵盖多个领域的知识库，包括科技、历史、文化、娱乐等方面，能够回应各种类型的问题。\n\n3.强大的问答能力：ChatGLMpro 具有出色的问答能力，能够理解用户的问题并给出准确的回答。\n\n4.个性化交互：ChatGLMpro 能够根据用户的语气和兴趣进行个性化交互，让用户感受到更加自然的对话体验。\n\n5.开放的接口：ChatGLMpro 还提供了开放的接口，方便其他应用程序和企业将其集成到自己的系统中。\n\n总的来说，ChatGLMpro 是一款高性能、智能化、多功能的聊天机器人，能够为企业和个人提供高效的智能化服务。总的来说，chatglm是一个智能、灵活、友好的AI助手，可以帮助用户解决各种问题和需求。\n\n",
)
chat_asy = LLM_base.build(llm_cfg6)

config6 = ExampleConfig(chat_asy, chat_asy)
# config = config6