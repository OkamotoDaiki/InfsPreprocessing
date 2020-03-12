def TransformMagnification(magnification):
    """
    Transform magnification type. float to str(n*10 div10)
    """
    return str(int(10*magnification)) + "div10"