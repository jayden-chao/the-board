from crewai import Agent, Crew, Process, Task
import yaml
import os
from dotenv import load_dotenv
from crewai import LLM

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
    
def get_agent_prompt(agent, category, agent_prompts, perspective="neutral"):
    prompt = agent_prompts['agents'][agent][category]
    return prompt.format(perspective=perspective)

def get_task_prompt(agent, category, task_prompts, perspective=""):
    prompt = task_prompts['tasks'][agent][category]
    return prompt.format(perspective=perspective)

agent_prompts = load_prompts('agents')
task_prompts = load_prompts('tasks')

class TheBoard():
    """TheBoard crew"""

    def __init__(self, perspective="neutral"):
        
        self.perspective = perspective
        
        # --- Agents ---

        self.generator = Agent(
            role=get_agent_prompt('generator','role',agent_prompts),
            goal=get_agent_prompt('generator', 'goal', agent_prompts, perspective=self.perspective),
            backstory=get_agent_prompt('generator', 'backstory', agent_prompts, perspective=self.perspective),
            memory=True,
            verbose=True,
            llm=llm
        )

        self.refiner = Agent(
            role=get_agent_prompt('refiner','role',agent_prompts),
            goal=get_agent_prompt('refiner','goal',agent_prompts, perspective=self.perspective),
            backstory=get_agent_prompt('refiner', 'backstory', agent_prompts, perspective=self.perspective),
            memory=True,
            verbose=True,
            llm=llm
        )

        self.translator = Agent(
            role=get_agent_prompt('translator','role',agent_prompts),
            goal=get_agent_prompt('translator','goal',agent_prompts, perspective=self.perspective),
            backstory=get_agent_prompt('translator', 'backstory', agent_prompts, perspective=self.perspective),
            memory=True,
            verbose=True,
            llm=llm
        )

        # --- Tasks ---

        self.base_response = Task(
            description=get_task_prompt('generator_task','description',task_prompts, perspective=self.perspective),
            expected_output=get_task_prompt('generator_task','expected_output',task_prompts, perspective=self.perspective),
            agent=self.generator
        )
        self.refined_response = Task(
            description=get_task_prompt('refiner_task','description',task_prompts, perspective=self.perspective),
            expected_output=get_task_prompt('refiner_task','expected_output',task_prompts, perspective=self.perspective),
            agent=self.refiner,
            context=[self.base_response]
        )
        self.translate_response = Task(
            description=get_task_prompt('translator_task','description',task_prompts, perspective=self.perspective),
            expected_output=get_task_prompt('translator_task','expected_output',task_prompts, perspective=self.perspective),
            agent=self.translator,
            context=[self.refined_response]
        )

        # --- Crew ---

        self.crew = Crew(
            agents=[self.generator, self.refiner, self.translator],
            tasks=[self.base_response, self.refined_response, self.translate_response],
            process=Process.sequential,
            verbose=True
        )


    def run_pipeline(self, user_input):

        inputs = {
            'user_input': user_input
        }

        return self.crew.kickoff(inputs=inputs)