from model import summary

def get_meeting_shortcut(input_text: str):
    context = f"Streść spotaknie z transkryptu, nie dodawaj nic od siebie, tylko streszczenie spotakania. Transkrypt:\n{input_text}"
    try:
        response = summary.llm.create_chat_completion(messages=[
            {
                "role": "user",
                "content": context
            }]
        )
    except ValueError:
        summary.double_n_ctx()
        response = get_meeting_shortcut(input_text)

    return response


def get_text_from_response(response) -> str:
    return response["choices"][0]["message"]["content"]
