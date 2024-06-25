from crewai import Agent, Crew, Process, Task  # type: ignore
from crewai.project import CrewBase, agent, crew, task  # type: ignore
from dotenv import load_dotenv
from serviceteam.tools.readData import DocsData
from serviceteam.tools.create_meeting import CreatMeeting
from serviceteam.tools.get_user_input import GetUserInput
from langchain_openai import ChatOpenAI
from serviceteam.tools.searchTool import SearchTool
load_dotenv()
@CrewBase
class ServiceteamCrew():
    """Serviceteam crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def Query_Handler(self) -> Agent:
        return Agent(
            config=self.agents_config['queryHandler'],
            tools=[DocsData.get_data_from_pdf, SearchTool.search_from_text],
            verbose=True,
        )

    @agent
    def Meeting_Creater(self) -> Agent:
        return Agent(
            config=self.agents_config['meetingCreater'],
            tools=[GetUserInput.get_input_for_meeting,CreatMeeting.create_meeting],
            verbose=True
        )

    @task
    def reading_task(self) -> Task:
        return Task(
            config=self.tasks_config['queryHandler'],
            agent=self.Query_Handler(),
        )

    @task
    def scheduling_meeting_task(self) -> Task:
        return Task(
            config=self.tasks_config['schedule_meeting_task'],
            agent=self.Meeting_Creater(),
            output_file='report2.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Serviceteam crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=2,
            process=Process.hierarchical,
            manager_llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        )
