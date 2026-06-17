from typing import TypedDict, Optional, List

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.modules.schemas.schema import ProgrammingProblem, CriticResponse
from app.modules.prompts.generator_prompt import GENERATOR_PROMPT
from app.modules.prompts.critic_prompt import CRITIC_PROMPT




llm = ChatGoogleGenerativeAI(
    model=settings.google_api_model,
    temperature=0.7,
    google_api_key=settings.google_api_key,
).with_structured_output(ProgrammingProblem)


critic_llm = ChatGoogleGenerativeAI(
    model=settings.google_api_model,
    temperature=0,
    google_api_key=settings.google_api_key,
).with_structured_output(CriticResponse)



class GeneratorAgent:
    def run(
        self,
        topic: str,
        difficulty: str,
        language: str,
    ) -> ProgrammingProblem:
        chain = GENERATOR_PROMPT | llm

        return chain.invoke({
            "topic": topic,
            "difficulty": difficulty,
            "language": language,
        })


class CriticAgent:
    def run(self, problem: ProgrammingProblem) -> CriticResponse:
        chain = CRITIC_PROMPT | critic_llm

        return chain.invoke({
            "problem_text": problem.model_dump_json(ensure_ascii=False)
        })


class GraphState(TypedDict):
    topic: List[str]
    difficulty: str
    language: str
    problem: Optional[ProgrammingProblem]
    critic_result: Optional[CriticResponse]
    feedback: Optional[str]
    round_count: int

class ProblemGenerationService:
    def __init__(self):
        self.generator = GeneratorAgent()
        self.critic = CriticAgent()

    @staticmethod
    def is_approved(critic_result: CriticResponse) -> bool:
        return critic_result.approved.strip().upper() == "APPROVED"

    def generate_node(self, state: GraphState):
        topic_text = ", ".join(state["topic"])

        if state.get("feedback") is None:
            problem = self.generator.run(
                topic=topic_text,
                difficulty=state["difficulty"],
                language=state["language"],
            )
        else:
            revised_topic = f"""
                            Chủ đề gốc:
                            {topic_text}

                            Độ khó:
                            {state["difficulty"]}

                            Ngôn ngữ:
                            {state["language"]}

                            Góp ý cần chỉnh:
                            {state["feedback"]}

                            Hãy chỉnh lại đề bài cho đầy đủ, rõ ràng và đúng chuẩn học thuật.
                            """

            problem = self.generator.run(
                topic=revised_topic,
                difficulty=state["difficulty"],
                language=state["language"],
            )

        print("\n--- Generated Problem ---\n")
        print(problem.model_dump_json(indent=2, ensure_ascii=False))
        print("\n-------------------------\n")

        return {
            "problem": problem,
            "round_count": state["round_count"] + 1,
        }

    def critic_node(self, state: GraphState):
        if state["problem"] is None:
            raise ValueError("Problem is missing before critic node")

        critic_result = self.critic.run(state["problem"])

        print("\n--- Critic Feedback ---\n")
        print(critic_result.model_dump_json(indent=2, ensure_ascii=False))
        print("\n-----------------------\n")

        return {
            "critic_result": critic_result,
            "feedback": critic_result.feedback,
        }

    def should_continue(self, state: GraphState) -> str:
        critic_result = state.get("critic_result")

        if critic_result and self.is_approved(critic_result):
            return "end"

        if state["round_count"] >= settings.loop_count:
            return "end"

        return "revise"

    def generate_problem(
        self,
        topic: List[str],
        difficulty: str,
        language: str,
    ) -> ProgrammingProblem:
        graph = StateGraph(GraphState)

        graph.add_node("generate", self.generate_node)
        graph.add_node("critic", self.critic_node)

        graph.set_entry_point("generate")

        graph.add_edge("generate", "critic")

        graph.add_conditional_edges(
            "critic",
            self.should_continue,
            {
                "end": END,
                "revise": "generate",
            },
        )

        app = graph.compile()

        result = app.invoke({
            "topic": topic,
            "difficulty": difficulty,
            "language": language,
            "problem": None,
            "critic_result": None,
            "feedback": None,
            "round_count": 0,
        })

        return result["problem"]