if __name__ == "__main__":
    # As in `Monorepo`
    
    try:
        from pip._internal.cli.main import main as pip_main
    except ModuleNotFoundError as exception:
        raise ModuleNotFoundError("Expected `--no-build-isolation`.") from exception

    def pip(*args):
        from importlib import reload
        import site
        
        return pip_main([
            "install",
            "--break-system-packages",
            *args
        ])
        reload(site)

    pip("setuptools")
    try:
        from setuptools import setup
    except ModuleNotFoundError:
        pip("setuptools")
        from setuptools import setup


    def install_utilities() -> None:
        """
        Bootstrap installation of the Utilities package.

        Attempt an editable install from the local repository if available;
        otherwise fall back to installing from the remote source.
        """
        from pathlib import Path

        # Prefer a local Utilities repo inside the monorepo if available
        # Locate the monorepo root that looks like .../src_and_submodules/monorepo
        here = Path(__file__).resolve()
        cur = here
        monorepo_root = None
        for _ in range(10):
            if cur.name == "monorepo" and cur.parent.name == "src_and_submodules":
                monorepo_root = cur
                break
            if cur.parent == cur:
                break
            cur = cur.parent

        local_repo = None
        if monorepo_root is not None:
            candidate = monorepo_root / "Utilities" / "build"
            if candidate.exists():
                local_repo = candidate

        if local_repo is not None and local_repo.exists():
            result = pip("--editable", str(local_repo))
            if result == 0:
                return
        elif __debug__:
            from warnings import warn
            warn(str(monorepo_root if monorepo_root is not None else here))
        pip("Utilities @ git+https://github.com/ArtificialHumanoid/Utilities.git#subdirectory=build")

    install_utilities()
    from utilities.management_of.resources.packages.installation import Requirements
    requirements, unparseable = Requirements(requirements="./requirements/.txt").load_requirements()

    # Differ from `Monorepo`

    import os

    if __debug__:
        print(os.getcwd())

    base_dir = os.path.dirname(__file__)

    readme_path = os.path.join(base_dir, "..", "README.md")
    try:
        with open(readme_path, "r", encoding="UTF-8") as fh:
            long_description = fh.read()
    except FileNotFoundError:
        long_description = ""


    setup(
        version="0.0.1",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=requirements
    )
