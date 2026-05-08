import argparse
from pathlib import Path


BACKEND_VALUES = Path("charts/hello-flask-backend/values.yaml")
FRONTEND_VALUES = Path("charts/hello-flask-frontend/values.yaml")


def replace_image(path: Path, image: str) -> None:
    lines = path.read_text().splitlines()
    updated = []
    replaced = False

    for line in lines:
        if line.startswith("image: "):
            updated.append(f"image: {image}")
            replaced = True
        else:
            updated.append(line)

    if not replaced:
        raise RuntimeError(f"No top-level image field found in {path}")

    path.write_text("\n".join(updated) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend-image", required=True)
    parser.add_argument("--frontend-image", required=True)
    args = parser.parse_args()

    replace_image(BACKEND_VALUES, args.backend_image)
    replace_image(FRONTEND_VALUES, args.frontend_image)


if __name__ == "__main__":
    main()
