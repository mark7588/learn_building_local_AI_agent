"""
Code guide for the main generation file:
- Imports the Ollama model wrapper and prompt template helper.
- Creates the local Ollama model used for generation.
- Defines the Korean recipe instruction block.
- Builds a prompt from the template.
- Connects the prompt to the model with a chain.
- Runs a sample request and prints the answer.
"""

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="qwen2.5")


template = """
당신은 한식 전문가이자 레시피 어시스턴트입니다.

반드시 {relevant_recipes}에 포함된 레시피만 사용하세요.
내장 지식이나 외부 상식으로 새로운 내용을 만들지 마세요.
사용자 질문에 가장 적합한 레시피를 정확히 하나만 선택해서 답변하세요.

규칙:
1. {relevant_recipes} 밖의 정보는 절대 사용하지 마세요.
2. 선택한 레시피는 하나만 제시하세요. 여러 개를 나열하지 마세요.
3. 답변은 선택한 레시피의 재료와 조리 순서만 바탕으로 작성하세요.
4. 질문이 {relevant_recipes}의 범위를 벗어나면 반드시 다음 문장만 답하세요: "I cannot answer your question"
5. 범위 안의 질문에는 간결하고 명확하게 답하세요.

사용자 요청: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model 

while True:
    question = input("질문을 입력하세요 (종료하려면 'exit' 입력): ")
    if question.lower() == 'exit':
        break
    
recipes = retriever.invoke(question)
result = chain.invoke({"relevant_recipes": recipes, "question": question})
print(result)