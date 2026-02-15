from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from groq import Groq
import os
import sys
from dotenv import load_dotenv
from face_verification.services.chat_services import save_chat, get_user_chats, clear_user_chats

load_dotenv()

# Initialize Groq client with API key from environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chatbot_stream(query, user_name):
    query=query+' answer in concise way in a paragraph.'+'my name is '+str(user_name)
    """Stream chatbot response from Groq API"""
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": query}],
        temperature=1,
        max_completion_tokens=800,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    # Stream the output
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            yield content

@never_cache
@login_required(login_url='face_login')
def chatbot_view(request):
    # Get chats from MongoDB
    chats_data = get_user_chats(request.user.username)
    chats = [{"user": chat["user_message"], "bot": chat["bot_response"]} for chat in chats_data]
    
    # Get user name from session (set by face recognition with recognized name) or fall back to Django user
    user_name = request.session.get('user_name') or request.user.first_name or request.user.get_full_name() or request.user.username
    
    # Debug: Print authenticated user info
    print(f"DEBUG - Session user_name: {request.session.get('user_name')}, Django user.first_name: {request.user.first_name}, Final user_name: {user_name}")

    if request.method == "POST":
        user_message = request.POST.get("message")
        
        # Collect streamed response
        bot_response = ""
        for chunk in chatbot_stream(user_message, user_name):
            bot_response += chunk
        
        # Save to MongoDB
        save_chat(request.user.username, user_message, bot_response)
        
        chats.append({
            "user": user_message,
            "bot": bot_response
        })

    return render(request, "chatbot/interface.html", {"chats": chats, "user_name": user_name})

@never_cache
def logout_view(request):
    # Explicitly flush session data to remove any stale user info
    request.session.flush()
    auth_logout(request)
    return redirect('home')

@login_required(login_url='face_login')
def clear_chat_view(request):
    """Clear all chats for the current user"""
    clear_user_chats(request.user.username)
    return redirect('chatbot:home')
