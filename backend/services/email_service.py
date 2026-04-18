DISPOSABLE_DOMAINS = ["tempmail.com", "mailinator.com"]

def is_disposable_email(email):
    domain = email.split("@")[-1]
    return domain in DISPOSABLE_DOMAINS