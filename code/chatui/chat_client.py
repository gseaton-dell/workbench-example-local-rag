"""The API client for the langchain-esque service."""
import logging

import mimetypes
import typing

import requests

# logging = logging.getLogger(__name__)
_LOGGER = logging.getLogger(__name__)

class ChatClient:
    """A client for connecting to the lanchain-esque service."""

    def __init__(self, server_url: str, model_name: str) -> None:
        """Initialize the client."""
        self.server_url = server_url
        self._model_name = model_name
        self.default_model = "llama2-7B-chat"

    @property
    def model_name(self) -> str:
        """Return the friendly model name."""
        return self._model_name

    def search(
        self, prompt: str
    ) -> typing.List[typing.Dict[str, typing.Union[str, float]]]:
        """Search for relevant documents and return json data."""
        data = {"content": prompt, "num_docs": 4}
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        url = f"{self.server_url}/documentSearch"
        logging.debug(
            "looking up documents - %s", str({"server_url": url, "post_data": data})
        )
        msg = str({"server_url": url, "post_data": data})
        print(f"making inference request - {msg}")

        with requests.post(url, headers=headers, json=data, timeout=30) as req:
            response = req.json()
            return typing.cast(
                typing.List[typing.Dict[str, typing.Union[str, float]]], response
            )

    def predict(
        self, query: str, use_knowledge_base: bool, num_tokens: int
    ) -> typing.Generator[str, None, None]:
        """Make a model prediction."""
        data = {
            "question": query,
            "context": "",
            "use_knowledge_base": use_knowledge_base,
            "num_tokens": num_tokens,
        }
        url = f"{self.server_url}/generate"
        logging.info(
            "making inference request - %s", str({"server_url": url, "post_data": data})
        )
        msg = str({"server_url": url, "post_data": data})
        print(f"making inference request - {msg} with context: {data['context']}")

        with requests.post(url, stream=True, json=data, timeout=10) as req:
            for chunk in req.iter_content(16):
                yield chunk.decode("UTF-8")

    def upload_documents(self, file_paths: typing.List[str]) -> None:
        """Upload documents to the kb."""
        url = f"{self.server_url}/uploadDocument"
        headers = {
            "accept": "application/json",
        }

        for fpath in file_paths:
            mime_type, _ = mimetypes.guess_type(fpath)
            # pylint: disable-next=consider-using-with # with pattern is not intuitive here
            files = {"file": (fpath, open(fpath, "rb"), mime_type)}

            logging.debug(
                "uploading file - %s",
                str({"server_url": url, "file": fpath}),
            )

            _ = requests.post(
                url, headers=headers, files=files, verify=False, timeout=30  # type: ignore [arg-type]
            )  # nosec # verify=false is intentional for now
