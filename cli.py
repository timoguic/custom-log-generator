import logging
import sys

import click
from tqdm import tqdm

from config import load_config
from providers import LogProvider

logger = logging.getLogger("clg")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("{name:20s} {levelname:8s} {message}", style="{"))
logger.addHandler(console_handler)


@click.command
@click.option(
    "--config",
    "-c",
    "filename",
    default="config.yaml",
    help="Config file with log generation settings.",
)
def make_logs(filename):
    """Main entrypoint - loads the config and generate logs

    filename is the path of the configuration file to read from"""

    conf = load_config(filename)

    log_provider = LogProvider(conf)

    fp = None
    if conf.get("output_file"):
        logger.debug("Opening output file...")
        fp = open(conf["output_file"], "w")

    logger.debug("Starting log generation...")
    for _ in tqdm(range(log_provider.count)):
        line = log_provider.generate()
        if fp is not None:
            # Write to file
            fp.write(line + "\n")
        else:
            # Write to stdout
            click.echo(line)

    if fp is not None:
        fp.close()


if __name__ == "__main__":
    make_logs()
