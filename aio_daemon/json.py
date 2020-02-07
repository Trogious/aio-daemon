import json

from .logging import Logger


def jl(json_obj):
    Logger.get_logger().error('\n' + json.dumps(json_obj, indent=2, sort_keys=True))
