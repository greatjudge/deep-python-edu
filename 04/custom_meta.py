def change_name(name, prefix='custom_'):
    if not (name.startswith('__') and name.endswith('__')):
        name = prefix + name
    return name


def add_prefix_to_attrs(attr_dict, prefix='custom_'):
    new_attr_dict = {}
    for name, value in attr_dict.items():
        new_attr_dict[change_name(name, prefix)] = value
    return new_attr_dict


class CustomMeta(type):
    def __new__(mcs, cls_name, bases, cls_dict):
        new_cls_dict = add_prefix_to_attrs(cls_dict)
        return super().__new__(mcs, cls_name, bases, new_cls_dict)

    def __init__(cls, cls_name, bases, cls_dict):
        def __setattr__(self, name, value):
            super(cls, self).__setattr__(change_name(name), value)

        super().__init__(cls_name, bases, cls_dict)
        cls.__setattr__ = __setattr__
