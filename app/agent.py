# ruff: noqa
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps.app import App
from .tools import get_user_data, save_session_data, book_schedule

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# --- Agent 3: Schedule Agent ---
schedule_agent = Agent(
    name="schedule_agent",
    model="gemini-2.5-flash-lite",
    description="Handles scheduling the next appointment.",
    instruction="""
    You are the scheduling assistant.
    1. Ask the user when they would like to come for their next session.
    2. Once they provide a date/time, use the `book_schedule` tool to register it.
    3. After booking, say "Looking forward to seeing you next time!" and end the conversation.
    """,
    tools=[book_schedule],
)

# --- Agent 2: Personal Trainer Agent ---
personal_trainer_agent = Agent(
    name="personal_trainer_agent",
    model="gemini-2.5-flash-lite",
    description="A personal trainer who conducts the training session and chat.",
    instruction="""
    You are a personal trainer.
    
    **Your Character:**
    {character}
    
    **User History:**
    {user_history}
    
    **Responsibilities:**
    1. Start the conversation based on your character and the user's history.
    2. Provide training advice, chat, and motivate the user.
    3. Keep track of the session's content.
    4. If the user indicates they want to finish (e.g., "I'm done", "That's enough", "See you"), do the following:
       - Summarize the session.
       - Call `save_session_data` with the summary.
       - Say goodbye and transfer the user to the `schedule_agent`.
    """,
    tools=[save_session_data],
    sub_agents=[schedule_agent],
)

# --- Agent 1: Receptionist Agent (Root) ---
root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash-lite",
    description="A personal trainer assistant",
    instruction="""
    You are the gym receptionist. Speak all in Japanese.
    1. Warmly greet the user with "Welcome back!" in Japanese.
    2. Ask for their name.
    3. Call the `get_user_data` tool with the provided name.
    4. If the user is found (tool returns success):
       - Tell them "I'll call your personal trainer now."
       - Transfer control to the `personal_trainer_agent`.
    5. If the user is NOT found:
       - Politely ask for the name again.
    """,
    tools=[get_user_data],
    sub_agents=[personal_trainer_agent],
)

app = App(root_agent=root_agent, name="app")
