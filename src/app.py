from crew import TheBoard


board = TheBoard(perspective="critical and mean")
    
user_query = input("Enter a message: ")
result = board.run_pipeline(user_query)

print("\n\n########################")
print("## FINAL OUTPUT ##")
print("########################\n")
print(result)