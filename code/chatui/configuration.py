"""The definition of the application configuration."""
from chatui.configuration_wizard import ConfigWizard, configclass, configfield


@configclass
class AppConfig(ConfigWizard):
    """Configuration class for the application.

    :cvar triton: The configuration of the chat server.
    :type triton: ChatConfig
    :cvar model: The configuration of the model
    :type triton: ModelConfig
    """

    server_url: str = configfield(
        "serverUrl",
        default="http://localhost",
        help_txt="The location of the chat API server.",
    )
    server_port: str = configfield(
        "serverPort",
        default="8000",
        help_txt="The port on which the chat server is listening for HTTP requests.",
    )
    server_prefix: str = configfield(
        "serverPrefix",
        default="/projects/retrieval-augmented-generation/applications/rag-api/",
        help_txt="The prefix on which the server is running.",
    )
    model_name: str = configfield(
        "modelName",
        default="llama2-7B-chat",
        help_txt="The name of the hosted LLM model.",
    )
