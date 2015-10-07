def patch_constance_fields():
    from ralph.admin.fields import MultilineField
    from constance.admin import FIELDS
    FIELDS[list] = FIELDS[tuple] = (MultilineField, {})


patch_constance_fields()
