from operator import itemgetter


def sort_messages_by_expiry(messages, reverese=True):
    return sorted(messages, key=itemgetter("expires_in"), reverse=reverese)
