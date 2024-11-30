import streamlit as st
import requests


def main():
    st.title("One-Day Tour Planning Assistant")

    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Function to append messages to chat history
    def add_to_chat_history(user_message, assistant_response):
        st.session_state.chat_history.append(
            {"user": user_message, "assistant": assistant_response}
        )

    # Callback function to clear input
    def clear_input():
        st.session_state.input = ""

    # Placeholder for chat history
    chat_history_placeholder = st.empty()

    # Function to display chat history
    def display_chat_history():
        chat_history_html = """
        <div id="chat-history" style="height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">
        """
        for chat in st.session_state.chat_history:
            chat_history_html += f"<p><b>You:</b> {chat['user']}</p>"
            chat_history_html += f"<p><b>Assistant:</b> {chat['assistant']}</p>"
        chat_history_html += "</div>"
        chat_history_html += """
        <script>
        var chatHistoryDiv = document.getElementById('chat-history');
        chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight;
        </script>
        """

        chat_history_placeholder.markdown(chat_history_html, unsafe_allow_html=True)

    # Display chat history initially
    display_chat_history()

    # Chat interface
    st.header("Chat with the Assistant")
    user_message = st.text_input("You: ", key="input")

    if st.button("Send"):
        if user_message:
            try:
                # Update the request to match the FastAPI endpoint
                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/travelplanner",
                    json={"message": user_message, "user_id": "user123"},
                )
                if response.status_code == 200:
                    assistant_response = response.json()["response"]
                    add_to_chat_history(user_message, assistant_response)
                    # Update chat history after receiving response
                    display_chat_history()
                    st.session_state.input = ""
                    # st.clear_input()
                else:
                    st.error(
                        f"Failed to get response. Status code: {response.status_code}, Response: {response.text}"
                    )
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")
        else:
            st.warning("Please enter a message.")


if __name__ == "__main__":
    main()
