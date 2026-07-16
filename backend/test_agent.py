from processminer.agents.process_agent import ProcessMiningAgent

agent = ProcessMiningAgent()

question = input("Ask FlowLens: ")

answer = agent.run(question)

print("\nAnswer:\n")
print(answer)