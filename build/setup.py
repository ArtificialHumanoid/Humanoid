import os


if __name__ == "__main__":
    from setuptools import setup
    from setuptools.config import expand

    if __debug__:
        print(os.getcwd())

    base_dir = os.path.dirname(__file__)

    readme_path = os.path.join(base_dir, "..", "README.md")
    try:
        with open(readme_path, "r", encoding="UTF-8") as fh:
            long_description = fh.read()
    except FileNotFoundError:
        long_description = ""

    def load_requirements(path):
        """Recursively load requirements from the given file."""
        result = []
        full_path = os.path.join(base_dir, path) if not os.path.isabs(path) else path
        try:
            with open(full_path, "r", encoding="UTF-8") as req_file:
                for line in req_file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("-r"):
                        nested = line[2:].strip()
                        nested_path = os.path.join(os.path.dirname(full_path), nested)
                        result.extend(load_requirements(nested_path))
                    else:
                        line = os.path.expandvars(line)
                        if line.startswith("git+"):
                            # Skip VCS dependencies for install_requires
                            continue
                        result.append(line)
        except FileNotFoundError:
            pass
        return result

    requirements = load_requirements("requirements_run.txt")

    # Monkey patch.


    def _assert_local(_, __):
        return True


    expand._assert_local = _assert_local


    setup(
        version="0.0.3",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=requirements,
    )
