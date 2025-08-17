if __name__ == "__main__":
    # As in `Monorepo`
    
    from pip._internal.cli.main import main as pip_main

    def pip(*args):
        return pip_main([
            "install",
            "--break-system-packages",
            *args,
        ])


    try:
        from setuptools import setup
    except ModuleNotFoundError:
        pip("setuptools")


    def install_utilities() -> None:
        """
        Bootstrap installation of the Utilities package.

        Attempt an editable install from the local repository if available;
        otherwise fall back to installing from the remote source.
        """
        from pathlib import Path
        from importlib import reload
        import site

        # As in `Utilities`'s `setup`
        build_dir = "build"
        local_repo = Path(__file__).resolve()
        while local_repo.name != build_dir:
            local_repo = local_repo.parent
        local_repo = local_repo.parent
        local_repo = local_repo / "src_and_submodules" / "monorepo" / "Utilities" /"build"
        if local_repo.exists():
            result = pip("--editable", str(local_repo))
            if result == 0:
                return
        elif __debug__:
            from warnings import warn
            warn(local_repo)
        pip("Utilities @ git+https://github.com/ArtificialHumanoid/Utilities.git#subdirectory=build")
        reload(site)

    install_utilities()
    from utilities.management_of.resources.packages.installation import Requirements
    requirements = Requirements(requirements="./requirements.txt").load_requirements()

    # Differ from `Monorepo`

    if __debug__:
        print(os.getcwd())

    base_dir = os.path.dirname(__file__)

    readme_path = os.path.join(base_dir, "..", "README.md")
    try:
        with open(readme_path, "r", encoding="UTF-8") as fh:
            long_description = fh.read()
    except FileNotFoundError:
        long_description = ""

    requirements = requirements.load_requirements()


    setup(
        version="0.0.1",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=requirements,
    )
