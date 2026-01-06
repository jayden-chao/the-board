from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import yaml
import os
from dotenv import load_dotenv
from crewai import LLM
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

load_dotenv()

api_key = os.getenv("API_KEY")
model = os.getenv("MODEL")

llm = LLM(
    model=model,
    temperature=1.0,
    api_key=api_key
)

def load_prompts(path):
    file = f"config/{path}.yaml"
    with open(file, 'r') as file:
        return yaml.safe_load(file)
    
def get_agent_prompt(agent, category, agent_prompts):
    prompt = agent_prompts['agents'][agent][category]
    return prompt

def get_task_prompt(agent, category, task_prompts):
    prompt = task_prompts['tasks'][agent][category]
    return prompt

agent_prompts = load_prompts('agents')
task_prompts = load_prompts('tasks')

class TheBoard():
    """TheBoard crew"""

    # --- Agents ---

    generator = Agent(
        role=get_agent_prompt('generator','role',agent_prompts),
        goal=get_agent_prompt('generator', 'goal', agent_prompts),
        backstory=get_agent_prompt('generator', 'backstory', agent_prompts),
        verbose=True,
        llm=llm
    )

    refiner = Agent(
        role=get_agent_prompt('refiner','role',agent_prompts),
        goal=get_agent_prompt('refiner','goal',agent_prompts),
        backstory=get_agent_prompt('refiner', 'backstory', agent_prompts),
        verbose=True,
        llm=llm
    )

    translator = Agent(
        role=get_agent_prompt('translator','role',agent_prompts),
        goal=get_agent_prompt('translator','goal',agent_prompts),
        backstory=get_agent_prompt('translator', 'backstory', agent_prompts),
        verbose=True,
        llm=llm
    )

    # --- Tasks ---

    base_response = Task(
        description=get_task_prompt('generator_task','description',task_prompts),
        agent=generator
    )
    refined_response = Task(
        description=get_task_prompt('refiner_task','description',task_prompts),
        agent=refiner,
        context=[base_response]
    )
    translate_response = Task(
        description=get_task_prompt('translator_task','description',task_prompts),
        agent=translator,
        context=[refined_response]
    )

    # --- Crew ---

    crew = Crew(
        agents=[generator, refiner, translator],
        tasks=[base_response, refined_response, translate_response],
        process=Process.sequential,
        verbose=True
    )

