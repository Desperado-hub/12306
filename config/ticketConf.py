# -*- coding: utf8 -*-
__author__ = 'MR.wen'
import json
import os

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def _get_yaml():
    """
    解析yaml
    :return: s  字典
    """
    config_dir = os.path.dirname(__file__)
    yaml_path = os.path.join(config_dir, 'ticket_config.yaml')
    json_path = os.path.join(config_dir, 'ticket_config.json')
    if yaml is not None:
        with open(yaml_path, encoding='utf-8') as f:
            return yaml.safe_load(f)
    with open(json_path, encoding='utf-8') as f:
        return json.load(f)


# def get_set_info():
#     return _get_yaml()["set"]
#
#
# def get_ticke_peoples():
#     return _get_yaml()["ticke_peoples"]
#
#
# def get_damatu():
#     return _get_yaml()["damatu"]
#
#
# print _get_yaml()["set"]["12306count"]