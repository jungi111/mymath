import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.globals import set_verbose
from langchain_teddynote.messages import stream_response

class MathProblemGenerator:
    def __init__(self):
        # .env 파일 로드
        load_dotenv()
        
        set_verbose(True)
        
        self.template = """
        Answer the user query.\n
        {format_instructions}\n
        {content}에 대한 수학 문제를 만들어주고, 그 문제에 대한 정답과 설명을 다음 형식으로 한글로 작성해 주세요.

        문제는 `question`에
        정답은 `answer`에
        설명은 `description`에 담아 주세요.
        """
        
        self.output_parser = JsonOutputParser()
        self.prompt = PromptTemplate.from_template(
            template=self.template, 
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        self.model = ChatOpenAI(
            temperature=0.7,
            max_tokens=400,
            model_name="gpt-3.5-turbo"
        )
        
        self.chain = self.prompt | self.model | self.output_parser
    
    def generate_question(self, content):
        input_data = {"content": content}
        response = self.chain.invoke(input_data)
        print(response)
        return response
