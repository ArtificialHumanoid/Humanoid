if __name__ == "__main__":
    import os
    from setuptools import setup
    from setuptools.config import expand

    def install_utilities() -> None:
        """
        Bootstrap installation of the Utilities package.

        Attempt an editable install from the local repository if available;
        otherwise fall back to installing from the remote source.
        """
        from pathlib import Path
        from importlib import reload
        import site
        from pip._internal.cli.main import main as pip_main

        # As in `Utilities`'s `setup`
        build_dir = "build"
        local_repo = Path(__file__).resolve()
        while local_repo.name != build_dir:
            local_repo = local_repo.parent
        local_repo = local_repo.parent
        local_repo = local_repo / "src_and_submodules" / "monorepo" / "Utilities" /"build"
        if local_repo.exists():
            pip_args = ["install", "--break-system-packages", "--editable", str(local_repo)]
            result = pip_main(pip_args)
            if result == 0:
                return
        elif __debug__:
            from warnings import warn
            warn(local_repo)
        pip_main([
            "install",
            "--break-system-packages",
            "Utilities @ git+https://github.com/ArtificialHumanoid/Utilities.git#subdirectory=build",
        ])
        reload(site)
    
    install_utilities()

    from utilities.management_of.resources.packages.installation import Requirements

    requirements = Requirements(requirements="./requirements_run.txt")

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

    # Monkey patch.


    def _assert_local(_, __):
        return True


    expand._assert_local = _assert_local


    setup(
        version="0.0.1",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=requirements,
    )
