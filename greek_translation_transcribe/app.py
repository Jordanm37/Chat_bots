import gradio as gr
import whisper
import os
from dotenv import load_dotenv
import openai

load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")

def transcribe_audio(audio_file):
    model = whisper.load_model("large")
    result = model.transcribe(audio_file)
    return result["text"]

def chatbot_completition(user_content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert Greek translator and transcription agent. Your role is to carefully examine the given text in Greek, identify semantic errors resulting from transcription, and then correct these errors. Use your knowledge of Greek language and syntax to ensure the accuracy and coherence of the transcriptions. Your task is crucial for the quality and usefulness of the transcriptions. You will be given Greek text that has been transcribed but may contain errors. Your job is to fix these errors to the best of your ability. Respond using markdown."},
            {"role": "user", "content": user_content},
        ],
    )
    return response["choices"][0]["message"]["content"]

def chatbot_completition_2(user_content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert Greek translator. Your role is to carefully examine the given text, which may be in different languages, and translate it accurately into Greek. Your translation work should account for not only literal translation but also cultural and contextual nuances. You'll be given text that has been translated into Greek, but it may contain errors due to literal or out-of-context translations. Your task is to correct these errors, ensuring the translated text preserves the original message while being grammatically correct and contextually appropriate in Greek.  Respond using markdown."},
            {"role": "user", "content": user_content},
        ],
    )
    return response["choices"][0]["message"]["content"]

# def handle_audio_inputs(audio_upload, audio_microphone):
#     if audio_upload is not None:
#         return audio_upload
#     else:
#         return audio_microphone

def main():
    audio_input = gr.inputs.Audio(source="upload", type="filepath")
    # audio_input_microphone = gr.inputs.Audio(source="microphone", type="filepath")

    output_text = gr.outputs.Textbox()

    transcription_interface = gr.Interface(
        fn= transcribe_audio,
        # inputs=[audio_input, audio_input_microphone],
        inputs=audio_input,
        outputs=output_text,
        title="Audio Transcription",
        description="Upload an audio file or record audio using the microphone, and hit the 'Submit' button.",
        live=True
    )

    with gr.Blocks() as chatbot_demo:
        chatbot = gr.Chatbot([], elem_id="chatbot").style(height=250)
        msg = gr.Textbox()
        clear = gr.Button("Clear")

        def respond(message, chat_history):
            bot_message = chatbot_completition(message)  # Use your chatbot_completition function here
            chat_history.append((message, bot_message))
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    with gr.Blocks() as chatbot_demo2:
        chatbot2 = gr.Chatbot([], elem_id="chatbot2").style(height=250)
        msg2 = gr.Textbox()
        clear2 = gr.Button("Clear")

        def respond2(message, chat_history):
            bot_message2 = chatbot_completition_2(message)  # Use your chatbot_completition function here
            chat_history.append((message, bot_message2))
            return "", chat_history

        msg2.submit(respond2, [msg2, chatbot2], [msg2, chatbot2])
        clear2.click(lambda: None, None, chatbot2, queue=False)

    tabbed_interface = gr.TabbedInterface([transcription_interface, chatbot_demo, chatbot_demo2], ["Transcription", "Chatbot transcription", "Chatbot translate"])

    tabbed_interface.launch(share=True)

if __name__ == '__main__':
    main()
    