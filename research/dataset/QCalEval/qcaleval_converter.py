# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/16 10:59:51
########################################################################

"""QCalEval dataset converter: parquet to JSON + PNG images."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pandas as pd


def load_parquet(parquet_path: str) -> pd.DataFrame:
    """Load QCalEval dataset from parquet file."""
    return pd.read_parquet(parquet_path)


def extract_images(
    df: pd.DataFrame,
    output_dir: Path,
    images_dir: Path = None,
) -> dict[str, str]:
    """Extract images from dataframe and save as PNG files.

    Returns a mapping from image_id to file path.
    """
    image_paths: dict[str, str] = {}
    images_dir = images_dir or (output_dir / "images")
    images_dir.mkdir(parents=True, exist_ok=True)

    # Check if 'images' column exists
    if "images" not in df.columns:
        # No images to extract, just return empty dict
        # Images should already exist from test set extraction
        return image_paths

    for idx, row in df.iterrows():
        images = row["images"]
        image_ids = row["image_ids"]

        # Handle pandas Series/array values
        if images is None or (hasattr(images, "__len__") and len(images) == 0):
            continue
        if image_ids is None or (hasattr(image_ids, "__len__") and len(image_ids) == 0):
            continue

        for img_data, img_id in zip(images, image_ids):
            if isinstance(img_data, dict) and "bytes" in img_data:
                img_bytes = img_data["bytes"]
                # Handle bytes or memoryview
                if hasattr(img_bytes, "tobytes"):
                    img_bytes = img_bytes.tobytes()

                img_path = images_dir / f"{img_id}.png"
                if not img_path.exists():
                    with open(img_path, "wb") as f:
                        f.write(img_bytes)
                image_paths[img_id] = str(img_path)

    return image_paths


def row_to_dict(row: pd.Series, image_paths: dict[str, str]) -> dict[str, Any]:
    """Convert a dataframe row to a dictionary."""
    # Handle both test and fewshot formats
    result: dict[str, Any] = {
        "id": row["id"],
        "experiment_type": row["experiment_type"],
    }

    # Optional fields that may not exist in fewshot
    if "experiment_family" in row.index:
        result["experiment_family"] = row["experiment_family"]
    if "experiment_background" in row.index:
        result["experiment_background"] = row["experiment_background"]
    if "source_id" in row.index:
        result["source_id"] = row["source_id"]

    # Add image paths
    image_ids = row["image_ids"]
    if hasattr(image_ids, "__len__") and len(image_ids) > 0:
        result["image_paths"] = [image_paths.get(iid, iid) for iid in image_ids]

    # Add questions and answers (q1-q6, handle missing columns)
    for i in range(1, 7):
        q_key = f"q{i}_prompt"
        a_key = f"q{i}_answer"
        if q_key in row.index and a_key in row.index:
            result[q_key] = row[q_key]
            result[a_key] = row[a_key]

    # Add key points and scoring
    if "q1_key_points" in row.index and isinstance(row["q1_key_points"], list):
        result["q1_key_points"] = row["q1_key_points"]
    if "q3_key_points" in row.index and isinstance(row["q3_key_points"], list):
        result["q3_key_points"] = row["q3_key_points"]
    if "q5_scoring" in row.index:
        result["q5_scoring"] = row["q5_scoring"]
    if "q6_expected_status" in row.index:
        result["q6_expected_status"] = row["q6_expected_status"]

    return result


def convert_parquet(
    parquet_path: str,
    output_dir: str,
    dataset_name: str = "test",
    images_dir: Path = None,
) -> None:
    """Convert QCalEval parquet to JSON + PNG images.

    Args:
        parquet_path: Path to input parquet file.
        output_dir: Output directory for JSON and images.
        dataset_name: Name of the dataset (used in output files).
        images_dir: Optional shared images directory.
    """
    parquet_path = Path(parquet_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    print(f"Loading {parquet_path}...")
    df = load_parquet(str(parquet_path))
    print(f"Loaded {len(df)} entries")

    # Extract images (use shared images_dir if provided)
    print("Extracting images...")
    image_paths = extract_images(df, output_dir, images_dir)
    print(f"Extracted {len(image_paths)} images")

    # Convert each row to JSON
    print("Converting to JSON...")
    converted_data = []
    for idx, row in df.iterrows():
        row_dict = row_to_dict(row, image_paths)
        converted_data.append(row_dict)

    # Save JSON
    output_json = output_dir / f"{dataset_name}.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(converted_data)} entries to {output_json}")
    print(f"Images saved to {output_dir / 'images'}")


def get_base_dir() -> Path:
    """Get the base directory for QCalEval dataset."""
    # resources/nvidia/QCalEval/qcaleval_converter.py -> project root
    return Path(__file__).parent.parent.parent.parent


def convert_test(parquet_path: str = None, output_dir: str = None) -> None:
    """Convert test set."""
    base_dir = get_base_dir() / "tmp" / "nvidia" / "QCalEval"
    parquet_path = parquet_path or str(base_dir / "test-00000-of-00001.parquet")
    output_dir = output_dir or str(base_dir / "converted")

    convert_parquet(parquet_path, output_dir, "test")


def convert_fewshot(parquet_path: str = None, output_dir: str = None) -> None:
    """Convert fewshot set."""
    base_dir = get_base_dir() / "tmp" / "nvidia" / "QCalEval"
    parquet_path = parquet_path or str(base_dir / "fewshot-00000-of-00001.parquet")
    output_dir = output_dir or str(base_dir / "converted")

    convert_parquet(parquet_path, output_dir, "fewshot")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert QCalEval dataset")
    parser.add_argument("--parquet", type=str, help="Input parquet file path")
    parser.add_argument("--output", type=str, help="Output directory")
    parser.add_argument("--name", type=str, default="test", help="Dataset name")
    parser.add_argument(
        "--test", action="store_true", help="Convert test set"
    )
    parser.add_argument(
        "--fewshot", action="store_true", help="Convert fewshot set"
    )

    args = parser.parse_args()

    if args.test:
        convert_test(args.parquet, args.output)
    elif args.fewshot:
        convert_fewshot(args.parquet, args.output)
    elif args.parquet:
        convert_parquet(args.parquet, args.output, args.name)
    else:
        # Default: convert both test and fewshot
        base_dir = get_base_dir() / "tmp" / "nvidia" / "QCalEval"
        output_dir = str(base_dir / "converted")

        print("=" * 50)
        print("Converting test set...")
        convert_test(output_dir=output_dir)

        print("=" * 50)
        print("Converting fewshot set...")
        convert_fewshot(output_dir=output_dir)