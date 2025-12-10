from google.adk.tools import ToolContext

# Mock Database
MOCK_DB = {
    "太郎": {
        "history": "前回はベンチプレスを40kgで10回3セット行いました。肩に少し痛みがあると言っていました。",
        "character": "名前はKenta、熱血トレーナー。好きな食べ物はラーメンでおすすめのラーメンを話すことがある。語尾は「だ！」や「筋肉が喜んでいるぞ！」などが特徴。"
    },
    "花子": {
        "history": "前回はヨガの基本ポーズを中心に、リラックス系のメニューでした。",
        "character": "名前はYukie、優しいお姉さんトレーナー。趣味はアニメ鑑賞で会話にアアニメ話題をを入れてくる。語尾は「ですね〜」「無理しないでね」が特徴。"
    }
}

def get_user_data(name: str, tool_context: ToolContext) -> dict:
    """Retrieves user history and character settings by name.

    Use this tool when the user provides their name to look up their records.

    Args:
        name: The name of the user.

    Returns:
        dict: A dictionary containing 'status' and optionally 'history' and 'character' if found.
    """
    if name in MOCK_DB:
        data = MOCK_DB[name]
        # Save to session state for other agents to use
        tool_context.state["user_history"] = data["history"]
        tool_context.state["character"] = data["character"]
        return {
            "status": "success",
            "message": f"User {name} found.",
            "history": data["history"],
            "character": data["character"]
        }
    else:
        return {
            "status": "error",
            "message": f"User {name} not found. Please ask for the name again."
        }

def save_session_data(summary: str, tool_context: ToolContext) -> dict:
    """Saves the session summary to the database.

    Use this tool to save the conversation or training log when the session is ending.

    Args:
        summary: A summary of the training session and conversation.

    Returns:
        dict: Status of the save operation.
    """
    # In a real app, this would write to a DB.
    # For now, we just log it or pretend.
    print(f"[MockDB] Saving session summary: {summary}")
    return {"status": "success", "message": "Session data saved."}

def book_schedule(date_time: str, tool_context: ToolContext) -> dict:
    """Registers the next appointment schedule.

    Use this tool when the user specifies a date and time for their next visit.

    Args:
        date_time: The date and time for the appointment (e.g., 'Next Tuesday at 10am').

    Returns:
        dict: Status of the booking.
    """
    print(f"[MockDB] Booking appointment for: {date_time}")
    return {"status": "success", "message": f"Appointment booked for {date_time}."}
