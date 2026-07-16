# from processminer.sql_tools.kpi import kpi_dashboard
# from processminer.sql_tools.bottleneck import bottleneck_analysis
# from processminer.sql_tools.resources import resource_analysis
# from processminer.sql_tools.variants import variant_analysis
# from processminer.sql_tools.sla import sla_detection

# #Rule base agent
# class ProcessMiningAgent:

#     def run(self, question):

#         question = question.lower()

#         if "kpi" in question:
#             return kpi_dashboard()

#         elif "bottleneck" in question or "delay" in question:
#             return bottleneck_analysis()

#         elif "resource" in question or "team" in question:
#             return resource_analysis()

#         elif "variant" in question or "path" in question:
#             return variant_analysis()

#         elif "sla" in question:
#             return sla_detection()

#         else:
#             return "I don't know which analysis tool to use."

# before is rule based agent
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from processminer.agents.tools import (
    kpi_tool,
    bottleneck_tool,
    resource_tool,
    variant_tool,
    sla_tool,
)

# Load environment variables
load_dotenv()

print("API Key:", os.getenv("GOOGLE_API_KEY"))


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
)

# Bind SQL tools to the LLM
llm_with_tools = llm.bind_tools([
    kpi_tool,
    bottleneck_tool,
    resource_tool,
    variant_tool,
    sla_tool,
])


class ProcessMiningAgent:

    def run(self, question: str):

        # Ask the LLM
        response = llm_with_tools.invoke(
            [HumanMessage(content=question)]
        )

        # If the model wants to call tools
        if response.tool_calls:

            tool_map = {
                "kpi_tool": kpi_tool,
                "bottleneck_tool": bottleneck_tool,
                "resource_tool": resource_tool,
                "variant_tool": variant_tool,
                "sla_tool": sla_tool,
            }

            results = []

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]

                tool = tool_map.get(tool_name)

                if tool:
                    output = tool.invoke({})
                    results.append(
                        f"{tool_name}:\n{output}"
                    )

            # Ask LLM to summarize the tool outputs
            final_prompt = f"""
User Question:
{question}

Tool Results:

{chr(10).join(results)}

Explain these results as a business report.
"""

            final_response = llm.invoke(final_prompt)

            return final_response.content

        # No tool needed
        return response.content


if __name__ == "__main__":

    agent = ProcessMiningAgent()

    while True:

        question = input("\nAsk: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = agent.run(question)

        print("\nAnswer:\n")
        print(answer)