import asyncio
import logging
import os
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)

HISTORY_FILENAME = "conversation_history.txt"

def load_history_from_file(filename: str) -> List[str]:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    return []

def save_history_to_file(history: List[str], filename: str = HISTORY_FILENAME) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(history))

class ChatBot:
    def __init__(self, model_name: str = "codellama", max_context_length: int = 50):
        """
        Initialize the chatbot with a specified language model and context length.
        
        Args:
            model_name (str): The name of the language model to use.
            max_context_length (int): Maximum number of conversation turns to retain for prompt generation.
        """
        # Initialize the language model
        self.llm = OllamaLLM(model=model_name, context_window = 160000)
        self.max_context_length = max_context_length
        
        # Load full conversation history from file (if available)
        self.full_history: List[str] = load_history_from_file(HISTORY_FILENAME)
        
        # Context history is a trimmed version for prompt generation
        if len(self.full_history) > self.max_context_length * 2:
            self.context_history = self.full_history[-self.max_context_length * 2:]
        else:
            self.context_history = self.full_history.copy()

        # System prompt with detailed instructions for the language model
        self.system_template = (
            "You are an expert Python dev. Provide concise, optimized, well-commented code. "
            "Answer user queries directly, with best practices. "
            "Conversation:\n{conversation_history}\n"
        )
        self.human_template = "User: {question}"

        # Create the chat prompt template from system and human messages
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_template),
            HumanMessagePromptTemplate.from_template(self.human_template)
        ])
        
        self.chain = self.prompt | self.llm

    def update_history(self, user_input: str, bot_response: str) -> None:
        """
        Update both the full conversation history and the context history with the latest exchange.
        
        Args:
            user_input (str): The user's input.
            bot_response (str): The assistant's response.
        """
        # Append to full_history (never trimmed)
        self.full_history.append(f"User: {user_input}")
        self.full_history.append(f"Assistant: {bot_response}")
        
        # Append to context_history (for prompt generation)
        self.context_history.append(f"User: {user_input}")
        self.context_history.append(f"Assistant: {bot_response}")
        
        # Truncate context_history if it exceeds the maximum allowed turns
        if len(self.context_history) > self.max_context_length * 2:
            self.context_history = self.context_history[-self.max_context_length * 2:]
            logging.info("Context history truncated to avoid context overflow.")

    async def generate_response(self, user_input: str) -> str:
        """
        Generate a response using the current context history.
        
        Args:
            user_input (str): The user's input message.
        
        Returns:
            str: The assistant's response.
        """
        history_str = "\n".join(self.context_history) if self.context_history else "None"
        try:
            # Run the chain invocation in a thread to avoid blocking
            response = await asyncio.to_thread(self.chain.invoke, {"question": user_input, "conversation_history": history_str})
        except Exception as e:
            logging.error("Error generating response: %s", e)
            return f"Error generating response: {e}"
        
        self.update_history(user_input, response)
        return response

async def main():
    chatbot = ChatBot(max_context_length=10)
    print("Welcome to the AI chatbot! Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            # Save the full conversation history (all turns) when exiting
            save_history_to_file(chatbot.full_history, HISTORY_FILENAME)
            print(f"Full conversation history saved to '{HISTORY_FILENAME}'.")
            break
        response = await chatbot.generate_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    asyncio.run(main())
