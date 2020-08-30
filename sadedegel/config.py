__all__ = ['set_config', 'get_config', 'describe_config', 'get_all_configs']

from typing import Any, Union
from functools import wraps
from collections import namedtuple
from .bblock.doc import Sentences
from .bblock.word_tokenizer import BertTokenizer, SimpleTokenizer

Configuration = namedtuple("Configuration", "config, description, valid_values")

configs = {
    "word_tokenizer": Configuration(config="word_tokenizer",
                                    description="Change the default word tokenizer used by sadedegel",
                                    valid_values=[BertTokenizer.name, SimpleTokenizer.name])
}


def check_config(f):
    @wraps(f)
    def wrapper(config, *args, **kwds):
        if config not in configs:
            raise Exception((f"{config} is not a valid configuration for sadegel."
                             "Use sadedegel.get_all_configs() to access list of valid configurations."))
        return f(*args, **kwds)

    return wrapper


def check_value(f):
    @wraps(f)
    def wrapper(config, value, *args, **kwds):
        cfg = configs.get(config, None)

        if cfg:
            if value not in cfg.valid_values:
                raise Exception(f"Valid values for {config} are {', '.join(cfg.valid_values)}.")
        else:
            raise Exception((f"{config} is not a valid configuration for sadegel."
                             "Use sadedegel.get_all_configs() to access list of valid configurations."))

        return f(*args, **kwds)

    return wrapper


@check_config
@check_value
def set_config(config: str, value: Any):
    if config == "word_tokenizer":
        Sentences.set_tokenizer(value)


@check_config
def get_config(config: str): # pylint: disable=inconsistent-return-statements
    if config == "word_tokenizer":
        return str(Sentences.tokenizer)


@check_config
def describe_config(config: str, print_desc=False) -> Union[None, str]: # pylint: disable=inconsistent-return-statements
    valid_values_fragment = "\n".join(configs[config].description)
    config_doc = f"""{configs[config].description}
                     
                     Valid values are {valid_values_fragment}
                 """

    if print_desc:
        print(config_doc)
    else:
        return config_doc


def get_all_configs():
    return configs
