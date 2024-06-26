import os
from dotenv import load_dotenv
from langchain_teddynote import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_teddynote.messages import stream_response

# .env 파일 로드
load_dotenv()

logging.langsmith(os.getenv('LANGCHAIN_PROJECT'))

template = """
{content}에 대한 수학 문제를 만들어주고, 그 문제에 대한 정답과 설명을 다음 형식으로 작성해 주세요.

문제는 `question`에
정답은 `answer`에
설명은 `description`에 담아 주세요.
"""

output_parser = JsonOutputParser()

prompt = PromptTemplate.from_template(template= template, partial_variables={"format_instructions": output_parser.get_format_instructions()})

input = {"content": "소인수분해"}

model = ChatOpenAI(
    temperature=0.7,
    max_tokens = 400,
    model_name="gpt-3.5-turbo"
)

chain = prompt | model | output_parser

response = chain.invoke(input)
print(response)