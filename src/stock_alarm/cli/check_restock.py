import typer

import logging
from typing import Optional

import yaml

from stock_alarm.webpage import request_via_proxy
from stock_alarm.report import send_notification, generate_report


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

app = typer.Typer()


@app.command()
def main(
    config_path: str = typer.Option(..., help="Path to the config file."),
    proxy_ip: Optional[str] = typer.Option(
        None, help="IP address of the proxy."
    ),
    port: Optional[str] = typer.Option(None, help="Port of the proxy."),
    report_output_path: str = typer.Option(..., help="Path of report."),
):
    # Read configs
    configs = {}
    with open(config_path, "r") as yaml_f:
        configs = dict(yaml.load(yaml_f, yaml.Loader))
    logging.info("Loaded configurations\n%s", str(configs))

    response_json = request_via_proxy(configs["target_url"], proxy_ip, port)

    # Generate report for posts
    generate_report(response_json, report_output_path)

    # Send notification about new items
    send_notification(response_json, configs["target_items"])


if __name__ == "__main__":
    app("stock-alarm")
