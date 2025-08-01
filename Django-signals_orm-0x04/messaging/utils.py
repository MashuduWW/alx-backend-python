
def get_thread(message):
    thread = []

    def recurse(msg, depth=0):
        thread.append((msg, depth))
        for reply in msg.replies.all().select_related('sender'):
            recurse(reply, depth + 1)

    recurse(message)
    return thread
