import functools

def get_partial_obj_fn(meta_information):
    if 'kwargs' in meta_information:
        obj_fn = functools.partial(meta_information['function'], **meta_information['kwargs'])
    else:
        obj_fn = meta_information['function']
    return obj_fn

def unwrap(obj_fn):
    def _unwraped(x):
        return obj_fn(x)[0]

    return _unwraped
