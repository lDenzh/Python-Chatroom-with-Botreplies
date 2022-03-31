import random


# Bot functions

def anakin(a, b=None):
    return "I think {} sounds intriguing".format(a + "ing")


def luke(a, b=None):
    if b is None:
        return "Not sure about {}. Don't I get a choice?".format(a + "ing")
    return "Sure, both {} and {} seems ok to me".format(a, b + "ing")


# A user function that allows communication with the bots

def user(a, b=None):
    print(a)
    return input("What is your response?: ")
