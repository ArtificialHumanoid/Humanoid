if __name__ == "__main__":
    import os
    from pathlib import Path

    from setuptools import setup


    def load_requirements(path: Path):
        requirements = []
        for line in path.read_text(encoding="UTF-8").splitlines():
            requirement = line.split("#", 1)[0].strip()
            if requirement and not requirement.startswith(("-", "--")):
                requirements.append(requirement)
        return requirements

    if __debug__:
        print(os.getcwd())

    base_dir = Path(__file__).resolve().parent
    requirements = load_requirements(base_dir / "requirements" / "run.txt")

    readme_path = base_dir.parent / "README.md"
    try:
        with readme_path.open("r", encoding="UTF-8") as fh:
            long_description = fh.read()
    except FileNotFoundError:
        long_description = ""


    setup(
        version="0.0.1",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=requirements
    )
