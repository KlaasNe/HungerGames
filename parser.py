from argparse import ArgumentParser


def make_parser() -> ArgumentParser:
    """Make the argument parser"""
    parser = ArgumentParser(
        description="Text-based hunger games simulator"
    )

    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Run the script in debug mode."
    )

    return parser
