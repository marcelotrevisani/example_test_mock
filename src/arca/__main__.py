import argparse
import logging
import sys
from typing import Union

import colorama
import pytest
from _pytest.config import ExitCode

colorama.init(autoreset=True)
logging.basicConfig(format="%(levelname)s:%(message)s")
log = logging.getLogger(__name__)


def main(args=None) -> Union[int, ExitCode]:
    if args is None:
        args = sys.argv[1:]
    log.debug(f"CLI cmds: {''.join(sys.argv)}")
    parser = argparse.ArgumentParser(description="-- ARCA --")


    args, pytest_args = parser.parse_known_args(args)
    return pytest.main(pytest_args)


if __name__ == "__main__":
    sys.exit(main())
