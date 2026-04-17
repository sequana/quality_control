import importlib.metadata as metadata


def get_package_version(package_name):
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return f"{package_name} not found"


version = get_package_version("sequana-quality-control")
