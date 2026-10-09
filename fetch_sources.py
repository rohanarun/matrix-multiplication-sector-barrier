"""Fetch the original sources at the revision and hashes in the manifest."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlparse
from urllib.request import urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manifest', type=Path,
                        default=Path(__file__).with_name('source-manifest.json'))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    repo = urlparse(manifest['repository'])
    if repo.scheme != 'https' or repo.netloc != 'github.com':
        raise ValueError('Expected an HTTPS GitHub repository')
    revision = manifest['commit']
    base = args.output.resolve()
    for entry in manifest['files']:
        relative = PurePosixPath(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Manifest path must remain within the output directory')
        target = base.joinpath(*relative.parts).resolve()
        if base not in target.parents:
            raise ValueError('Output path escapes the destination')
        if target.exists():
            data = target.read_bytes()
        else:
            url = ('https://raw.githubusercontent.com' + repo.path.rstrip('/')
                   + '/' + quote(revision, safe='') + '/' + quote(str(relative)))
            with urlopen(url, timeout=60) as response:
                data = response.read()
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError(f'Hash mismatch: {relative}; existing files are not overwritten')
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(f"Verified {len(manifest['files'])} pinned upstream source files")


if __name__ == '__main__':
    main()
