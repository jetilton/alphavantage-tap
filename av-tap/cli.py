import click


from .get_data import get_data

BASEURL = "https://www.alphavantage.co/"
APIKEY = "254HSAHQEDW8E1AD"


@click.command()
@click.option("--config", "-c")
@click.option("state_file", "-st")
def tap(config, state_file):

    data = get_data(BASEURL, config, APIKEY)


if __name__ == "main":
    tap()