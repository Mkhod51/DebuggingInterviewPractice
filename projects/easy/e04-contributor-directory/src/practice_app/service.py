"""Public profile rendering and directory search."""
from .models import load_contributors, validate_quality
from .directory import Directory


def display_quality(contributor, default):
    validate_quality(default)
    if default is None:
        raise ValueError("Display default must be numeric")
    return contributor.quality or default


def render_profile(contributor, default):
    result = contributor.as_dict()
    result["display_quality"] = display_quality(contributor, default)
    result["quality_known"] = contributor.quality is not None
    return result


class DirectoryService:
    def __init__(self, directory, default_quality=0.5):
        validate_quality(default_quality)
        if default_quality is None:
            raise ValueError("Display default must be numeric")
        self.directory = directory
        self.default_quality = default_quality

    def profile(self, identifier):
        contributor = self.directory.get(identifier)
        return None if contributor is None else render_profile(contributor, self.default_quality)

    def by_email(self, email):
        contributor = self.directory.find_email(email)
        return None if contributor is None else render_profile(contributor, self.default_quality)

    def search(self, text):
        return [render_profile(row, self.default_quality) for row in self.directory.search(text)]

    def summary(self):
        rows = self.directory.all()
        return dict(total=len(rows), active=sum(row.active for row in rows),
                    quality_known=sum(row.quality is not None for row in rows))


def service_from_file(path):
    return DirectoryService(Directory(load_contributors(path)))
