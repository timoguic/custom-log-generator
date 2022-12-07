import click
from tqdm import tqdm

from config import load_config
from providers import LogProvider


@click.command
@click.option(
    "--config",
    "-c",
    "filename",
    default="config.yaml",
    help="Config file with log generation settings.",
)
def make_logs(filename):
    conf = load_config(filename)

    log_provider = LogProvider(conf)

    fp = None
    if conf.get("output_file"):
        fp = open(conf["output_file"], "w")

    print("Generating logs...")
    for _ in tqdm(range(log_provider.count)):
        line = log_provider.generate()
        if fp is not None:
            fp.write(line + "\n")
        else:
            print(line)

    if fp is not None:
        fp.close()


if __name__ == "__main__":
    make_logs()
