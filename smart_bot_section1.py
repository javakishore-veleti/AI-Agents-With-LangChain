from dotenv import load_dotenv
from importlib.metadata import version
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import traceable
from typing import List, Dict
from pydantic import BaseModel, Field
import os

load_dotenv(override=True)

_ls_key = os.getenv("LANGSMITH_API_KEY", "")
print(f"[debug] cwd={os.getcwd()}")
print(f"[debug] LANGSMITH_API_KEY={_ls_key[:12]}...{_ls_key[-6:]} (len={len(_ls_key)})")
print(f"[debug] LANGSMITH_ENDPOINT={os.getenv('LANGSMITH_ENDPOINT', '(default)')}")

if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ.setdefault("LANGSMITH_PROJECT", "Smart Q&A Bot Project")
    print("LangSmith tracing enabled.")


class QAResponse(BaseModel):
    answer: str = Field(..., description="The answer to the question")
    confidence: str = Field(..., description="Confidence Level: High, Medium, Low")
    reasoning: str = Field(..., description="The reasoning behind the answer")
    follow_up_questions: List[str] = Field(default_factory=list, description="List of follow-up questions")
    sources_needed: bool = Field(description="Whether sources are needed for the answer", default=False)


# noinspection PyTypeChecker
class SmartQABot:
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        self.model = ChatOpenAI(model=model_name, temperature=temperature).with_structured_output(QAResponse)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant that answers questions in a structured format. "
                    "Provide the answer, confidence level, reasoning, follow-up questions, and whether sources are"
                ),
                (
                    "human",
                    "{question}"
                )
            ]
        )
        self.chain = self.prompt | self.model

    @traceable(name="SmartQABot.ask", run_type="chain", tags=["qa", "structured_response"])
    def ask(self, question: str) -> QAResponse:
        try:
            """Ask a question and get a structured response"""
            return self.chain.invoke({"question": question})
        except Exception as e:
            print(f"Error during question answering: {e}")
            return QAResponse(
                answer="Sorry, I couldn't process your question.",
                confidence="Low",
                reasoning=str(e),
                follow_up_questions=[],
                sources_needed=False
            )

    @traceable(name="SmartQABot.ask_batch", run_type="chain", tags=["qa", "structured_response", "batch"])
    def ask_batch(self, questions: List[str]) -> List[QAResponse]:
        """Ask a batch of questions and get structured responses"""
        batch_inputs = [{"question": q} for q in questions]
        try:
            return self.chain.batch(batch_inputs)
        except Exception as e:
            print(f"Error during batch question answering: {e}")
            return [QAResponse(
                answer="Sorry, I couldn't process your question.",
                confidence="Low",
                reasoning=str(e),
                follow_up_questions=[],
                sources_needed=False
            ) for _ in questions]


def demo_smart_qa_bot():
    bot = SmartQABot()
    question = "What is the capital of France?"
    response = bot.ask(question)
    print(f"Response for single question: {response}")

    batch_questions = [
        "What is the capital of France?",
        "What is the largest mammal?",
        "What is the capital of India?"
    ]
    batch_responses = bot.ask_batch(batch_questions)
    for i, resp in enumerate(batch_responses):
        print(f"Response for question {i+1}: {resp}")

if __name__ == "__main__":
    demo_smart_qa_bot()