from dash import Dash, html, dcc, Input, Output, State
from openai import OpenAI

# OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

app = Dash(__name__)

app.layout = html.Div(
    style={"width": "50%", "margin": "auto", "fontFamily": "Arial"},
    children=[
        html.H2("💻 IT Engineer Chatbot"),

        dcc.Textarea(
            id="user-input",
            placeholder="Ask an IT or computer-related question...",
            style={"width": "100%", "height": "100px"}
        ),

        html.Br(),
        html.Button("Ask", id="ask-btn", n_clicks=0),

        html.Hr(),
        html.Div(id="chat-output", style={"whiteSpace": "pre-wrap"})
    ]
)

@app.callback(
    Output("chat-output", "children"),
    Input("ask-btn", "n_clicks"),
    State("user-input", "value")
)
def get_response(n_clicks, user_input):
    if not user_input:
        return ""

    messages = [
        {
            "role": "system",
            "content": (
                "You are an IT engineer assistant. Answer only IT and computer related content. "
                "If the question is not IT related reply exactly: "
                "'Only IT and computer related question i can answer i am a IT engineer assistant.'"
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-4",
        messages=messages,
        temperature=0,
        max_tokens=150
    )

    return "Bot: " + response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)
