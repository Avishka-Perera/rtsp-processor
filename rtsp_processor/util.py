import importlib
import cv2
import numpy as np

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

class AspectSaveResize:
    def __init__(self, inp_shape, out_shape, crop_offset=[0, 0]) -> None:
        if out_shape[0] / out_shape[1] > inp_shape[0] / inp_shape[1]:
            crop_h = inp_shape[0]
            crop_w = round(crop_h / out_shape[0] * out_shape[1])
        else:
            crop_w = inp_shape[1]
            crop_h = round(crop_w / out_shape[1] * out_shape[0])

        start = [round((inp_shape[0] - crop_h) / 2), round((inp_shape[1] - crop_w) / 2)]
        start = [max(0, start[0] + crop_offset[0]), max(0, start[1] + crop_offset[1])]
        end = [
            min(inp_shape[0], start[0] + crop_h),
            min(inp_shape[1], start[1] + crop_w),
        ]
        start = [end[0] - crop_h, end[1] - crop_w]

        self.slice_h = slice(start[0], end[0])
        self.slice_w = slice(start[1], end[1])
        self.resize_shape = out_shape
        self.crop_shape = [crop_h, crop_w]
        self.crop_start = start

    def __call__(self, img: np.ndarray) -> np.ndarray:
        img = img[self.slice_h, self.slice_w, :]
        img = cv2.resize(img, self.resize_shape[::-1])
        return img
