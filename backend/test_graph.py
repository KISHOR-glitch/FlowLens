from processminer.agents.graph import graph


while True:

    question = input("Ask: ")

    if question == "exit":
        break

    result = graph.invoke({

        "question": question

    })

    print()
    print(result["answer"])