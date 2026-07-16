from processminer.agents.graph import graph

while True:

    question = input("\nAsk FlowLens: ")

    if question.lower() in ["exit", "quit"]:
        break

    result = graph.invoke({
        "question": question,
        "tool_calls": [],
        "tool_results": [],
        "answer": ""
    })

    print("\n==========================")
    print(result["answer"])
    print("==========================")