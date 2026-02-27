from typing import Iterator
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessageChunk
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel, Field
import langchain

langchain.debug = True
load_dotenv()





class Slogan(BaseModel):
    """A movie with details."""
    flower_name: str = Field(..., description="flower name")
    price: int = Field(..., description="price")
    slogan: str = Field(..., description="slogan")


parser: JsonOutputParser = JsonOutputParser(pydantic_object=Slogan)
model = init_chat_model("gpt-5.2")
# model = init_chat_model("claude-sonnet-4-5-20250929")
prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
    ("system", "您是一位专业的鲜花店文案撰写员。"),
    ("human", "对于售价为 {price} 元的 {flower_name}，您能提供一个吸引人的Slogan吗？，请严格按照以下格式返回JSON：\n{format_instructions}")
]).partial(format_instructions=parser.get_format_instructions())
chain: RunnableSerializable = prompt | model

flowers: list[str] = ["玫瑰", "百合", "康乃馨"]
prices: list[str] = ["50", "30", "20"]

for flower, price in zip(flowers, prices):
    outputs: Iterator[AIMessageChunk] = chain.stream({"flower_name": flower, "price": price})
    full: AIMessageChunk | None = None
    for chunk in outputs:
        full = chunk if full is None else full + chunk
        print(full.content_blocks)
    print(full.content_blocks)
    result: dict = parser.invoke(full)
    print(result)


