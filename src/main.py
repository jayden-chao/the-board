#!/usr/bin/env python
import sys
import warnings
import json

from crew import TheBoard

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(inputs):
    """
    Run crew given inputs
    """

    inputs = inputs

    try:
        TheBoard().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"Error occured while running crew! :(")

def train(n_iters, filename, inputs=None):
    inputs = inputs

    return TheBoard().crew().train(n_iterations=n_iters, filename=filename, inputs=inputs)

def replay(task_id):
    """
    Replay crew execution from a specific task
    """
    return TheBoard().crew().replay(task_id=task_id)

def test(n_iterations, eval_llm, inputs=None):
    """Test the crew for n_iterations with a specific LLM."""
    inputs = inputs
    return TheBoard().crew().test(n_iterations=n_iterations, eval_llm=eval_llm, inputs=inputs)

def run_with_trigger(trigger_json):
    """Run the crew using a JSON trigger payload."""
    try:
        trigger_payload = json.loads(trigger_json)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON payload provided")
    
    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }
    return run(inputs)




# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         TheBoard().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         TheBoard().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }

#     try:
#         TheBoard().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")

# def run_with_trigger():
#     """
#     Run the crew with trigger payload.
#     """
#     import json

#     if len(sys.argv) < 2:
#         raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

#     try:
#         trigger_payload = json.loads(sys.argv[1])
#     except json.JSONDecodeError:
#         raise Exception("Invalid JSON payload provided as argument")

#     inputs = {
#         "crewai_trigger_payload": trigger_payload,
#         "topic": "",
#         "current_year": ""
#     }

#     try:
#         result = TheBoard().crew().kickoff(inputs=inputs)
#         return result
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew with trigger: {e}")
