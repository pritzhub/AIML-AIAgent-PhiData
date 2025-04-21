from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.tools.postgres import PostgresTools
from phi.tools.email import EmailTools

load_dotenv()

# Initialize PostgresTools with connection details
postgres_tools = PostgresTools(
    host="localhost",
    port=5432,
    db_name="dbName",
    user="postgres", 
    password="dbPassword",
)

receiver_email = "xxx@gmail.com"
sender_email = "xxx@gmail.com"
sender_name = "xxx yyy"
sender_passkey = "<sender_passkey>"

# Create an agent with the PostgresTools
agent_postgres = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[postgres_tools],
    instructions=["Alwats include sources","Use table to display the data"],
    debug_mode=True,
)

# Create an agent with the EmailTools
agent_email = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    #model=OpenAIChat(id="gpt-4o"),
    tools=[
        EmailTools(
            receiver_email=receiver_email,
            sender_email=sender_email,
            sender_name=sender_name,
        )
    ],
    instructions=["Alwats include sources"],
    debug_mode=True,
)

agent_team = Agent(
    team=[agent_postgres, agent_email],
    model=Groq(id="llama-3.3-70b-versatile"),
    #model=OpenAIChat(id="gpt-4o"),
    show_tool_calls=True,
    markdown=True,
    instructions=["Alwats include sources"],
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response in the terminal
#agent_team.print_response("Summarize and compare analyst recommendations and fundamentals for TSLA and NVDIA. Also share the latest news for NVDA", stream=True)

# Example: Ask the agent to run a SQL query
#agent_postgres.print_response("Please run a SQL query to get first 5 data from the lntds_analog_data. Use table to display the data, and use the actual table columns",)

agent_team.print_response("Please run a SQL query to get first 5 data from the lntds_analog_data")

#agent_email.print_response("Send an email to say Hello")
