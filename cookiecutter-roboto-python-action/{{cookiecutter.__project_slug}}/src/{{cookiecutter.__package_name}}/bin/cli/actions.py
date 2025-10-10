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


class VerbosityAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        kwargs.setdefault("default", logging.ERROR)
        kwargs.setdefault("nargs", 0)
        super().__init__(option_strings, dest, **kwargs)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | collections.abc.Sequence[typing.Any] | None,
        option_string: str | None = None,
    ):
        current_level = getattr(namespace, self.dest, logging.ERROR)
        new_level = max(current_level - 10, logging.DEBUG)
        setattr(namespace, self.dest, new_level)
