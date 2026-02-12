from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

document = [
    "India has income tax law.",
    "Tax is calculated based on income tax slabs.",
    "GST is 18% for many goods."
]

document_text = "\n".join(document)

question = "What is GST?"

response = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct",
    max_tokens=150,
    temperature=0,
    messages=[
        {"role": "system", "content": "Answer only from the given document."},
        {"role": "user", "content": f"Document:\n{document_text}\n\nQuestion:\n{question}"}
    ],
)

print(response.choices[0].message.content)
