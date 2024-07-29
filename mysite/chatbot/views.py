from django.shortcuts import render
from .models import Message
import requests
import os


def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        bot_message = get_ai_response(user_message)
        Message.objects.create(
            user_message=user_message, 
            bot_message=bot_message
            )
    messages = Message.objects.all()
    return render(request, 'chatbot/chat.html', {'messages': messages})


def get_ai_response(user_input: str) -> str:
    # Set up the API endpoint and headers
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }

    # Data payload
    messages = get_existing_messages()
    messages.append({
        "role": "user", 
        "content": f"{user_input}"
        })
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.7
    }
    response = requests.post(
        endpoint, 
        headers=headers, 
        json=data
        )
    response_data = response.json()

    # Check if there's an error in the response
    if 'error' in response_data:
        print("Error in API response:", response_data['error'])
        return "Sorry, I encountered an error."

    print(f'{response_data = }')
    ai_message = response_data['choices'][0]['message']['content']
    return ai_message

def get_existing_messages() -> list:
    """
    Get all messages from the database and format them for the API.
    """
    formatted_messages = []

    for message in Message.objects.values('user_message', 'bot_message'):
        formatted_messages.append({
            "role": "user", 
            "content": message['user_message']
            })
        formatted_messages.append({
            "role": "assistant", 
            "content": message['bot_message']
            })

    return formatted_messages
