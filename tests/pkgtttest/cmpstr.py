"""Checks for Finder values"""


def str_get_dirtrk(dirtrk_exp, finder):
    """Pretty print if assertion fails"""
    dirtrk_act = finder.get_dirtrk()
    return (
        "\n"
        f"EXP: {dirtrk_exp}\n"
        f"ACT: {dirtrk_act}\n"
        f"ACT: {finder}")
