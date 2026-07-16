from typing import TypedDict

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

from processminer.agents.process_agent import llm, llm_with_tools

from processminer.agents.tools import (
    bottleneck_tool,
    kpi_tool,
    process_discovery_tool,
    resource_tool,
    sla_tool,
    variant_tool,
)

# -----------------------------
# Graph State
# -----------------------------

class ProcessState(TypedDict):
    question: str
    tool_calls: list
    tool_results: list
    answer: str


# -----------------------------
# Tool Map
# -----------------------------

tool_map = {
    "bottleneck_tool": bottleneck_tool,
    "kpi_tool": kpi_tool,
    "process_discovery_tool": process_discovery_tool,
    "resource_tool": resource_tool,
    "sla_tool": sla_tool,
    "variant_tool": variant_tool,
}


# -----------------------------
# Node 1 - Question
# -----------------------------

def question_node(state: ProcessState):

    print("\nQuestion:")
    print(state["question"])

    return state


# -----------------------------
# Node 2 - Planner
# Gemini decides which tools to call
# -----------------------------

def planner_node(state: ProcessState):

    response = llm_with_tools.invoke(
        [HumanMessage(content=state["question"])]
    )

    print("\nTool Calls:")
    print(response.tool_calls)

    state["tool_calls"] = response.tool_calls

    return state


# -----------------------------
# Node 3 - Execute Tools
# -----------------------------

def execute_tool_node(state: ProcessState):

    results = []

    for tool_call in state["tool_calls"]:

        tool_name = tool_call["name"]

        tool = tool_map.get(tool_name)

        if tool:

            output = tool.invoke({})

            results.append({
                "tool": tool_name,
                "result": output
            })

    state["tool_results"] = results

    return state


# -----------------------------
# Node 4 - Summary
# -----------------------------

def summary_node(state: ProcessState):

    prompt = f"""
You are an AI Process Mining Consultant.

User Question:
{state["question"]}

SQL Tool Results:
{state["tool_results"]}

Write a professional report containing:

1. Summary
2. Findings
3. Recommendations
"""

    response = llm.invoke(prompt)

    state["answer"] = response.content

    return state


# -----------------------------
# Build Graph
# -----------------------------

builder = StateGraph(ProcessState)

builder.add_node("question", question_node)
builder.add_node("planner", planner_node)
builder.add_node("execute_tools", execute_tool_node)
builder.add_node("summary", summary_node)

builder.set_entry_point("question")

builder.add_edge("question", "planner")
builder.add_edge("planner", "execute_tools")
builder.add_edge("execute_tools", "summary")
builder.add_edge("summary", END)

graph = builder.compile()