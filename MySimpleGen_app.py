import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI   # fixed import

# 1. Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
print(f"Using OpenAI API Key:{openai_api_key}")

# 2. Initialize the LLM (ChatGPT style model)
llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.7, model="gpt-3.5-turbo")

# 3. Define a simple prompt template
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="You are a helpful assistant. Answer clearly:\n\n{user_input}"
)

# 4. Create the chain
chain = LLMChain(llm=llm, prompt=prompt)

# 5. Run the bot
if __name__ == "__main__":
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye! 👋")
            break

        response = chain.invoke({"user_input": user_query})
        print("Bot:", response["text"])  # <-- extract only the text
