CHAT_PROMPT_TEMPLATE = """
You are a helpful travel assistant. 
User message: {message}
Respond naturally and guide the user about their travel plan.
"""

PLAN_PROMPT_TEMPLATE = """
Create a detailed {days}-day travel itinerary based on the user's preferences: {preferences}.
Output the plan day-by-day with timings and short notes.
"""

# Function to build prompts using the templates
def build_prompt(template: str, **kwargs) -> str:
    return template.format(**kwargs)
