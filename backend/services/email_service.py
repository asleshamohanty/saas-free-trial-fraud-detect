DISPOSABLE_DOMAINS = {
    "tempmail.com",
    "10minutemail.com",
    "mailinator.com"
}


def is_disposable_email(email):
    domain = email.split("@")[-1].lower()
    return domain in DISPOSABLE_DOMAINS


def normalize_email(email):
    email = email.strip().lower()

    if "@" not in email:
        return email

    local, domain = email.split("@", 1)

    # Only Gmail-style canonicalization
    if domain in {"gmail.com", "googlemail.com"}:
        local = local.split("+")[0]
        local = local.replace(".", "")

    return f"{local}@{domain}"