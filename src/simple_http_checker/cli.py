import logging
import click
from .checker import check_urls

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

print(f"cli.py: {__name__}")

@click.command()
@click.argument("urls", nargs=-1) #nargs == number of args with -1 == unlimited
@click.option("--timeout", default=5, help="Timeout in seconds for each request.")
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
def main(urls, timeout, verbose):

    if verbose:
        logger.debug("Verbose logging enabled")
        logging.getLogger().setLevel(logging.DEBUG) #Set level from root logger
    if not urls:
        logger.warning("NO URLs provided.")
        click.echo("Usage: check-urls <URL1> <URL2> ....")
        return

    logger.info(f"urls: {urls}")
    logger.info(f"timeout: {timeout}s")
    logger.info(f"verbose: {verbose}")
    logger.info(f"Starting checks for {len(urls)} URLs.")

    results = check_urls(urls, timeout=3)

    click.echo("\n----Results----")
    for url, status in results.items():
        if "OK" in status:
            text_colour = "green"
        else:
            text_colour="red"
        click.secho(f"{url:<40} -> {status}", fg=text_colour)

