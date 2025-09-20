def default_role(context):
    if context.get_current_parameters()["id"] == 1:
        return "admin"
    else:
        return "member"