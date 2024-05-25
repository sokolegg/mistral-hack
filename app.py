import gradio as gr
from transformers import pipeline

pipeline = pipeline(task="image-classification", model="julien-c/hotdog-not-hotdog")

def predict(input_txt):
    predictions = pipeline(input_img)
    return input_img, {p["label"]: p["score"] for p in predictions} 

gradio_app = gr.Interface(
    predict,
    inputs=[gr.Text(label="Doctor's input")],
    outputs=[gr.Text(label="Processed Summary")],
    title="Create summary of the medical appointment.",
)

if __name__ == "__main__":
    gradio_app.launch()
