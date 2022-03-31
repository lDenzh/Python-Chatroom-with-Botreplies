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

#if a in exciting_things:
  #      return "YESS! Time for {}".format(action)
  #  elif action in boring_things:
 #       return "What? {} sucks. Not doing that.".format(action)
#    return "I don't care!"

#