def inspect_obj(obj: object) -> None:
    """Inspect object and print to Console

    Args:
        obj (object): Object to inspect
    """
    from pprint import pprint

    pprint(vars(obj))
