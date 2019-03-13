from app import app

print("hi from filters")

@app.template_filter()
def possessive_form(s):
    """
    Give off the prossessive form of the string, assumed to be a noun. No
    guarantees are made when this filter is used on a string that is not a noun.
    """
    if s.endswith("s"):
        return "%s'" % s
    else:
        return "%s's" % s
