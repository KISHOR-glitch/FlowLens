from typing import TypedDict

from langgraph.graph import StateGraph, END

from processminer.agents.process_agent import ProcessMiningAgent


class ProcessState(TypedDict):
    question: str
    answer: str


agent = ProcessMiningAgent()


def process_node(state: ProcessState):

    answer = agent.run(state["question"])

    return {
        "question": state["question"],
        "answer": answer
    }


builder = StateGraph(ProcessState)

builder.add_node("process_agent", process_node)

builder.set_entry_point("process_agent")

builder.add_edge("process_agent", END)

graph = builder.compile()