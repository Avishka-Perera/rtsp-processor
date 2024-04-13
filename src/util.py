import importlib


def load_class(target):
    """loads a class using a target"""
    *module_name, class_name = target.split(".")
    module_name = ".".join(module_name)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls


def make_obj_from_conf(conf, **kwargs):
    cls = load_class(conf["target"])
    params = conf["params"] if "params" in conf else {}
    obj = cls(**params, **kwargs)
    return obj
