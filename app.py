from flask import Flask, request, jsonify, session
from flask_session import Session
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


app.config['SESSION_TYPE'] = 'filesystem'
# Change this to a secure random value in your production application
app.config['SECRET_KEY'] = 'super secret key'
Session(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/chat', methods=['POST'])
def chat():
    # force=True ensures parsing as JSON even if Content-Type header is not set
    data = request.get_json(force=True)
    user_input = data.get('input')
    if not user_input:
        return 'Bad Request', 400
    # user_input = request.get_json('input', force=True)
    print('user', user_input)
    messages = session.get('messages', [])

    # Join the previous messages with the new user input
    prompt = '\n'.join(messages + [f'User: {user_input}'])

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )

    messages.append(f'User: {user_input}')
    messages.append(f'AI: {response.choices[0].text.strip()}')

    # Save the updated message history in the session
    session['messages'] = messages
    print(messages)

    return jsonify(response.choices[0].text.strip())


if __name__ == '__main__':
    app.run(debug=True)
