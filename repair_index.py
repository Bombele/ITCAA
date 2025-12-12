# repair_index.py
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Any

import json
import faiss  # ignored via mypy.ini


def load_index(index_path: Path) -> Optional[faiss.Index]:
    """Load a FAISS index from disk, or return None if not found."""
    if not index_path.exists():
        return None
    return faiss.read_index(str(index_path))


def save_index(index: faiss.Index, index_path: Path) -> None:
    """Persist FAISS index to disk."""
    faiss.write_index(index, str(index_path))


def load_meta(meta_path: Path) -> List[Dict[str, Any]]:
    """Load metadata JSON adjacent to the index, or return empty list."""
    if not meta_path.exists():
        return []
    with open(meta_path, "r", encoding="utf-8") as f:
        data: List[Dict[str, Any]] = json.load(f)
    return data


def save_meta(meta: List[Dict[str, Any]], meta_path: Path) -> None:
    """Persist metadata JSON adjacent to the index."""
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


def repair_index(index_path: Path) -> None:
    """
    Minimal repair routine:
    - loads index and metadata
    - performs a basic integrity check
    - writes back if needed
    """
    index = load_index(index_path)
    if index is None:
        raise FileNotFoundError(f"Index not found at {index_path}")

    meta_path = index_path.with_suffix(".meta.json")
    meta: List[Dict[str, Any]] = load_meta(meta_path)

    # Example: ensure each entry has an 'id' and 'text' field
    repaired: List[Dict[str, Any]] = []
    for entry in meta:
        eid = entry.get("id")
        text = entry.get("text")
        if isinstance(eid, (str, int)) and isinstance(text, str):
            repaired.append(entry)

    if len(repaired) != len(meta):
        save_meta(repaired, meta_path)
        print(f"Repaired metadata entries: {len(meta) - len(repaired)} removed")

    # Optionally re-write index (no-op here)
    save_index(index, index_path)
    print("Index repair completed.")


def main() -> None:
    # Default path; adjust via CLI if needed
    idx = Path("build/index.faiss")
    repair_index(idx)


if __name__ == "__main__":
    main()