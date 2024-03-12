"""The definition of the application configuration."""
from chain_server.configuration_wizard import ConfigWizard, configclass, configfield


@configclass
class MilvusConfig(ConfigWizard):
    """Configuration class for the Milvus connection.

    :cvar url: URL of Milvus DB
    """

    url: str = configfield(
        "url",
        default="http://localhost:9091",
        help_txt="The host of the machine running Milvus DB",
    )


# @configclass
# class TritonConfig(ConfigWizard):
#     """Configuration class for the Triton connection.

#     :cvar server_url: The location of the Triton server hosting the llm model.
#     :cvar model_name: The name of the hosted model.
#     """

#     server_url: str = configfield(
#         "server_url",
#         default="localhost:8001",
#         help_txt="The location of the Triton server hosting the llm model.",
#     )
#     model_name: str = configfield(
#         "model_name",
#         default="ensemble",
#         help_txt="The name of the hosted model.",
#     )


@configclass
class AppConfig(ConfigWizard):
    """Configuration class for the application.

    :cvar milvus: The configuration of the Milvus vector db connection.
    :type milvus: MilvusConfig
    :cvar triton: The configuration of the backend Triton server.
    :type triton: TritonConfig
    """

    milvus: MilvusConfig = configfield(
        "milvus", env=False, default="http://127.0.0.1:19530", help_txt="The configuration of the Milvus connection."
    )
    # triton: TritonConfig = configfield(
    #     "triton",
    #     env=False,
    #     help_txt="The configuration for the Triton server hosting the embedding models.",
    # )
