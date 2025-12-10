import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from app.agent import root_agent
from google.genai import types as genai_types

async def main():
    print("--- Starting Agent Test ---")
    session_service = InMemorySessionService()
    session_id = "test_session_001"
    user_id = "test_user"
    
    await session_service.create_session(
        app_name="app", user_id=user_id, session_id=session_id
    )
    
    runner = Runner(
        agent=root_agent, app_name="app", session_service=session_service
    )

    # 1. Start Conversation
    print("\n[User]: (Connects)")
    # Usually the agent starts if the user sends an empty message or we just say "Hello"
    query = "Hello" 
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=genai_types.Content(
            role="user", 
            parts=[genai_types.Part.from_text(text=query)]
        ),
    ):
        if event.is_final_response():
            print(f"[Agent]: {event.content.parts[0].text}")

    # 2. Provide Name
    print("\n[User]: 太郎です")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=genai_types.Content(
            role="user", 
            parts=[genai_types.Part.from_text(text="太郎です")]
        ),
    ):
        if event.is_final_response():
            print(f"[Agent]: {event.content.parts[0].text}")
            
    # 3. Chat with Trainer
    print("\n[User]: 今日は調子がいいです")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=genai_types.Content(
            role="user", 
            parts=[genai_types.Part.from_text(text="今日は調子がいいです")]
        ),
    ):
        if event.is_final_response():
            print(f"[Agent]: {event.content.parts[0].text}")

    # 4. End Session
    print("\n[User]: 今日はもう終わりで")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=genai_types.Content(
            role="user", 
            parts=[genai_types.Part.from_text(text="今日はもう終わりで")]
        ),
    ):
        if event.is_final_response():
            print(f"[Agent]: {event.content.parts[0].text}")

    # 5. Schedule
    print("\n[User]: 来週の火曜日10時にお願いします")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=genai_types.Content(
            role="user", 
            parts=[genai_types.Part.from_text(text="来週の火曜日10時にお願いします")]
        ),
    ):
        if event.is_final_response():
            print(f"[Agent]: {event.content.parts[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
