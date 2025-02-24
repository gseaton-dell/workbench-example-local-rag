"""Entrypoint for the Conversation GUI.

The functions in this module are responsible for bootstrapping then executing the Conversation GUI server.
"""

import argparse
import os
import sys
import logging

import uvicorn

from . import bootstrap_logging

_LOG_FMT = f"[{os.getpid()}] %(asctime)15s [%(levelname)7s] - %(name)s - %(message)s"
_LOG_DATE_FMT = "%b %d %H:%M:%S"
_LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the program.

    :returns: A namespace containing the parsed arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="Document Retrieval Service")

    parser.add_argument(
        "--help-config",
        action="store_true",
        default=False,
        help="show the configuration help text",
    )

    parser.add_argument(
        "-c",
        "--config",
        metavar="CONFIGURATION_FILE",
        default="/dev/null",
        help="path to the configuration file (json or yaml)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=1,
        help="increase output verbosity",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="decrease output verbosity",
    )

    parser.add_argument(
        "--host",
        metavar="HOSTNAME",
        type=str,
        default="0.0.0.0",  # nosec # this is intentional
        help="Bind socket to this host.",
    )
    parser.add_argument(
        "--port",
        metavar="PORT_NUM",
        type=int,
        default=8080,
        help="Bind socket to this port.",
    )
    parser.add_argument(
        "--workers",
        metavar="NUM_WORKERS",
        type=int,
        default=1,
        help="Number of worker processes.",
    )
    parser.add_argument(
        "--ssl-keyfile", metavar="SSL_KEY", type=str, default=None, help="SSL key file"
    )
    parser.add_argument(
        "--ssl-certfile",
        metavar="SSL_CERT",
        type=str,
        default=None,
        help="SSL certificate file",
    )

    cliargs = parser.parse_args()
    if cliargs.help_config:
        # pylint: disable=import-outside-toplevel; this is intentional to allow for the environment to be configured
        #                                          before any of the application libraries are loaded.
        from chatui.configuration import AppConfig

        sys.stdout.write("\nconfiguration file format:\n")
        AppConfig.print_help(sys.stdout.write)
        sys.exit(0)

    return cliargs


if __name__ == "__main__":
    args = parse_args()
    os.environ["APP_VERBOSITY"] = f"{args.verbose - args.quiet}"
    os.environ["APP_CONFIG_FILE"] = args.config

    from chatui import api, chat_client, configuration, pages

    # load config
    config_file = os.environ.get("APP_CONFIG_FILE", "/dev/null")
    config = configuration.AppConfig.from_file(config_file)
    if not config:
        sys.exit(1)

    # configure logging
    bootstrap_logging(2)

    # connect to other services
    api_url = f"{config.server_url}:{config.server_port}"
    print(api_url)
    client = chat_client.ChatClient(api_url, config.model_name)
    proxy_prefix = os.environ.get("PROXY_PREFIX")
    blocks = pages.converse.build_page(client)
    blocks.queue(max_size=10)
    blocks.launch(server_name="0.0.0.0", server_port=8080, root_path=proxy_prefix)
