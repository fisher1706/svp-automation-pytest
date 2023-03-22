def get_suite_name_from_params(params: tuple):
    for i, param in enumerate(params):
        if param == '-m':
            return params[i + 1]
    return None
