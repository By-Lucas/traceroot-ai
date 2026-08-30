import os


def region():
    return os.environ["PAYMENT_REGION"]  # PAYMENT_REGION is accessed without startup validation
