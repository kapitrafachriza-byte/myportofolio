def is_editor(user):
    """Cek apakah user termasuk dalam grup 'Editor'."""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name="Editor").exists()


def is_owner(user):
    """Cek apakah user adalah pemilik portofolio (superuser)."""
    if not user.is_authenticated:
        return False
    return user.is_superuser


def can_edit(user):
    """Editor ATAU superuser boleh mengedit."""
    return is_editor(user) or is_owner(user)


def can_create_or_delete(user):
    """Hanya superuser yang boleh membuat atau menghapus."""
    return is_owner(user)
