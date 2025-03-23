import streamlit as st
import datetime
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
from langchain_groq import ChatGroq

if 'questions' not in st.session_state:
    st.session_state.questions = []
# Function to handle chatbot responses (optional)
def get_bot_response(user_input):
  llm = ChatGroq(model="gemma2-9b-it", groq_api_key= groq_api_key)
  return llm.invoke(user_input).content


# Sidebar with menu
st.sidebar.title("Chose an option")
sidebar_option = st.sidebar.radio("Choose an option:", ["Schedule a Meeting", "Chat with Bot","Post your question to experts" ,"Show your questions"])
st.title("conNEcT")
# Main app layout
if sidebar_option == "Schedule a Meeting":
    st.header("Meeting Scheduler")
  # Input for participants' emails
    participants = st.text_area("Enter Participants' Email (comma separated)")
    # Date and Time Picker for scheduling a meeting
    meeting_date = st.date_input("Select Meeting Date", min_value=datetime.date.today())
    meeting_time = st.time_input("Select Meeting Time", datetime.time(9, 0))

    # Calculate the meeting datetime
    meeting_datetime = datetime.datetime.combine(meeting_date, meeting_time)

    # Duration input (in minutes)
    duration = st.slider("Meeting Duration (minutes)", 15, 180, 30)

    # Button to confirm and display scheduled meeting details
    if st.button("Schedule Meeting"):
        st.success(f"🎉 Meeting Scheduled Successfully and added to Google Calendar!")
        st.write(f"**Meeting Date & Time**: {meeting_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Duration**: {duration} minutes")
        st.write(f"**Meeting End Time**: {(meeting_datetime + timedelta(minutes=duration)).strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Attendees**: {', '.join(participants)}")
elif sidebar_option == "Chat with Bot":
    st.header("Chat with Virtual Assistant")

    # Text input for chatting with the bot
    user_input = st.text_input("Ask a question:")

    # If the user asks something, show a response
    if user_input:
        st.session_state.questions.append(user_input)
        # Uncomment below to integrate OpenAI GPT for dynamic responses
        bot_response = get_bot_response(user_input)

        # Static response for the chatbot
        #bot_response = "I'm your assistant! How can I help with your questions about meetings or anything else?"

        st.write(f"**Bot:** {bot_response}")

elif sidebar_option == "Post your question to experts":
  st.header("Post your question")
  question = st.text_area("What question do you have our experts?")
  if st.button("Submit"):
    st.session_state.questions.append(question)

elif sidebar_option == "Show your questions":

  if st.session_state.questions:
      st.write("### Previous Questions:")
      for idx, question in enumerate(st.session_state.questions, 1):
          st.write(f"{idx}. {question}")
