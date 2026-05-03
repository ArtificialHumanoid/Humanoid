from __future__ import annotations

import hashlib
import os
import shutil
import stat
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ACT_VERSION = "0.2.88"
ACT_ASSET = "act_Linux_x86_64.tar.gz"
ACT_ASSET_SHA256 = "1eb9996682dfcc053ac8f3f90f2ec50376f0cdfc229712d82da03d673c63a2b3"
ACT_BINARY_SHA256 = "a76aa7627c633f5e9e9b06407d6eb1069213b1ee984599381b84ad4e7bd894f0"
ACT_URL = f"https://github.com/nektos/act/releases/download/v{ACT_VERSION}/{ACT_ASSET}"


def _default_data_home() -> Path:
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download(url: str, destination: Path) -> None:
    with urllib.request.urlopen(url, timeout=60) as response:
        with destination.open("wb") as handle:
            shutil.copyfileobj(response, handle)


def _ensure_archive(archive_path: Path) -> None:
    if archive_path.exists() and _sha256(archive_path) == ACT_ASSET_SHA256:
        return

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=archive_path.parent, delete=False) as download:
        temporary_path = Path(download.name)

    try:
        _download(ACT_URL, temporary_path)
        actual_sha256 = _sha256(temporary_path)
        if actual_sha256 != ACT_ASSET_SHA256:
            raise RuntimeError(
                f"Unexpected SHA-256 for {ACT_ASSET}: {actual_sha256}"
        )
        temporary_path.replace(archive_path)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _ensure_binary(archive_path: Path, binary_path: Path) -> None:
    if binary_path.exists() and _sha256(binary_path) == ACT_BINARY_SHA256:
        binary_path.chmod(binary_path.stat().st_mode | stat.S_IXUSR)
        return

    binary_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=binary_path.parent, prefix=".act-", delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)

    with tarfile.open(archive_path, "r:gz") as archive:
        member = archive.getmember("act")
        extracted = archive.extractfile(member)
        if extracted is None:
            raise RuntimeError(f"{ACT_ASSET} did not contain an act binary.")

        try:
            with temporary_path.open("wb") as handle:
                shutil.copyfileobj(extracted, handle)

            actual_sha256 = _sha256(temporary_path)
            if actual_sha256 != ACT_BINARY_SHA256:
                raise RuntimeError(
                    f"Unexpected SHA-256 for extracted act binary: {actual_sha256}"
                )

            temporary_path.chmod(temporary_path.stat().st_mode | stat.S_IXUSR)
            temporary_path.replace(binary_path)
        finally:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass


def _link_binary(binary_path: Path, link_path: Path) -> None:
    link_path.parent.mkdir(parents=True, exist_ok=True)
    if link_path.exists() or link_path.is_symlink():
        if link_path.resolve() == binary_path:
            return
        raise RuntimeError(
            f"{link_path} already exists and does not point to {binary_path}."
        )
    link_path.symlink_to(binary_path)


def main() -> int:
    install_root = Path(
        os.environ.get(
            "HUMANOID_ACT_HOME",
            _default_data_home() / "humanoid" / "tools" / "nektos-act",
        )
    )
    version_dir = install_root / f"v{ACT_VERSION}"
    archive_path = version_dir / ACT_ASSET
    binary_path = version_dir / "act"

    _ensure_archive(archive_path)
    _ensure_binary(archive_path, binary_path)

    bin_dir = Path(
        os.environ.get("HUMANOID_ACT_BIN_DIR", Path.home() / ".local" / "bin")
    )
    link_path = bin_dir / "act"
    _link_binary(binary_path, link_path)

    print(f"Installed act {ACT_VERSION}: {binary_path}")
    print(f"Linked act: {link_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
