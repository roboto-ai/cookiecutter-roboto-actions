import argparse
import collections.abc
import logging
import typing


class KeyValuePairsAction(argparse.Action):
    value_dict: dict[str, typing.Any] = {}

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | collections.abc.Sequence[typing.Any] | None,
        option_string: str | None = None,
    ):
        if values is None:
            return

        try:
            for pair in values:
                key, value = pair.split("=")

                if key in self.value_dict:
                    raise parser.error(
                        f"'{key}' was defined multiple times for '{self.dest}'"
                    )

                self.value_dict[key] = value

            setattr(namespace, self.dest, self.value_dict)
        except Exception as e:
            raise parser.error(
                f"Failed to parse '{self.dest}' argument '{values}': {e}"
            )


class LogLevelAction(argparse.Action):
    """Convert string log level choices to their corresponding logging constants."""

    LEVEL_MAP = {
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | collections.abc.Sequence[typing.Any] | None,
        option_string: str | None = None,
    ):
        if values is None:
            return

        if isinstance(values, str):
            level_str = values.lower()
            if level_str in self.LEVEL_MAP:
                setattr(namespace, self.dest, self.LEVEL_MAP[level_str])
            else:
                parser.error(
                    f"Invalid log level '{values}'. Choose from: {', '.join(self.LEVEL_MAP.keys())}"
                )
