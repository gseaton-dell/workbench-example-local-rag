"""This module contains the chatui gui for chat."""
from pathlib import Path
from typing import List

import gradio as gr

from chatui import assets, chat_client

PATH = "/kb"
TITLE = "Knowledge Base Management"


def build_page(client: chat_client.ChatClient) -> gr.Blocks:
    """Buiild the gradio page to be mounted in the frame."""
    kui_theme, kui_styles = assets.load_theme("kaizen")

    with gr.Blocks(title=TITLE, theme=kui_theme, css=kui_styles) as page:
        # create the page header
        gr.Markdown(f"# {TITLE}")

        with gr.Row():
            upload_button = gr.UploadButton(
                "Add File", file_types=["pdf"], file_count="multiple"
            )
        with gr.Row():
            file_output = gr.File()

        # form actions
        upload_button.upload(
            lambda files: upload_file(files, client), upload_button, file_output
        )

    page.queue()
    return page


def upload_file(files: List[Path], client: chat_client.ChatClient) -> List[str]:
    """Use the client to upload a file to the knowledge base."""
    file_paths = [file.name for file in files]
    client.upload_documents(file_paths)
    return file_paths
