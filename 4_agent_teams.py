from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
#from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

### Custom sybmols declarations - Custom code - it can be any python code. Also, can be written in another file such as yfinance and reference in this program
### yfinance is nothing but a Python program with APIs and instructions

def get_company_symbol(company: str) -> str:
    """Use this function to get the symbol for a company.
    
    Args:
        company (str): The name of the company.
        
    Returns:
        str: The symbol for the company.
    """
    symbols = {
        "Phidata": "MSFT",
        "Infosys": "INFY",
        "Tesla": "TSLS",
        "Apple": "AAPL",
    }
    return symbols.get(company, "Unknown")

web_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    #model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    show_tool_calls=True,
    markdown=True,
    instructions=["Always include sources","Use bullets as * than numbers to display data."],
    debug_mode=True,
)

finance_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    #model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True), get_company_symbol],
    show_tool_calls=True,
    markdown=True,
    instructions=["Use tables to display data.",
    "If you don't know the company symbol, please use get_company_symbol tool, even if it is not a public company"],
    debug_mode=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    #model=OpenAIChat(id="gpt-4o"),
    show_tool_calls=True,
    markdown=True,
    instructions=["Use tables to display data.","Alwats include sources","If you don't know the company symbol, please use get_company_symbol tool, even if it is not a public company"],
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response in the terminal
agent_team.print_response("Summarize and compare analyst recommendations and fundamentals for TSLA and NVDIA. Also share the latest news for NVDA", stream=True)