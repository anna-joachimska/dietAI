from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.messages import SystemMessage, HumanMessage
from prompts import system
from tools import fatsecret

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

llm_with_tools = llm.bind_tools(tools=[fatsecret.get_breakfast_recipe, fatsecret.get_lunch_recipe, fatsecret.get_main_dish_recipe])

def generate_response(calories:int, user_preferences: str):
    messages = [
        SystemMessage(system.MEAL_PLANNER_SYSTEM_PROMPT),
        HumanMessage(f"Generate a meal plan with:\n Calories: {calories}\n User preferences: {user_preferences}")
    ]

    tools_response = llm_with_tools.invoke(messages)

    messages.append(tools_response)

    ai_msg = llm_with_tools.invoke(messages)

    # selected_tool = {"get_recipes": fatsecret.get_recipes}[tools_response.tool_calls["name"]]
    for tool_call in ai_msg.tool_calls:
        selected_tool = {"get_breakfast_recipe": fatsecret.get_breakfast_recipe,
                         "get_lunch_recipe": fatsecret.get_lunch_recipe,
                         "get_main_dish_recipe": fatsecret.get_main_dish_recipe}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    response = llm_with_tools.invoke(messages)

    messages.append(response)

    for message in messages:
        print(message.pretty_print())

    return response.content