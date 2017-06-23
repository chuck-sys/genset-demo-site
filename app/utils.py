
# Variables
SAMPLE_FILES = [
    ('Y. pestris', 'https://github.com/'),
    ('S. dysenteriae', 'https://github.com/'),
    ('S. typhimurium', 'https://github.com/'),
    ('P. syringae', 'https://github.com/'),
    ('X. campestris', 'https://github.com/'),
    ('C. trachematis', 'https://github.com/'),
    ('S. fredii', 'https://github.com/'),
]

# Functions
def sid_is_valid(sid):
    '''
    Checks to see if the session ID is valid or not. Valid session IDs do not
    contain slashes of any kind, and should not attempt to do any directory
    traversal.

    Temporarily fix: Only works for SIDs with a length of < 10.
    '''
    if '/' in sid or '\\' in sid:
        return False

    # FIXME: Only works for SIDs with length < 10
    if len(sid) >= 10:
        return False

    return True