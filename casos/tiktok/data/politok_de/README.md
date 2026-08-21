---
license: cc-by-4.0
task_categories:
  - text-classification
  - video-classification
language:
  - de
tags:
  - tiktok
  - politics
  - social-media
  - germany
  - multimodal
  - content-moderation
size_categories:
  - 100K<n<1M
configs:
  - config_name: saxony_2024_post_ids
    data_files:
      - split: train
        path: data/saxony_2024/post_ids.parquet
  - config_name: federal_2025_post_ids
    data_files:
      - split: train
        path: data/federal_2025/post_ids.parquet
  - config_name: saxony_2024_annotations
    data_files:
      - split: train
        path: data/saxony_2024/annotations.parquet
---

# PoliTok-DE

A Multimodal Dataset of Political TikToks and Deletions From Germany.

**Paper:** [PoliTok-DE: A Multimodal Dataset of Political TikToks and Deletions From Germany](https://arxiv.org/abs/2509.15860)

**Authors:** Tomas Ruiz, Andreas Nanz, Ursula Kristin Schmid, Carsten Schwemmer, Yannis Theocharis, Diana Rieger

## Dataset Description

PoliTok-DE contains TikTok post IDs from two German elections:

| Collection | Window | Released post IDs | Deleted at re-scrape |
|---|---:|---:|---:|
| Saxony state election 2024 | 2024-07-01 to 2024-11-30 | 195,373 | 36,617 (18.7%) |
| German federal election 2025 | 2025-01-13 to 2025-04-30 | 743,588 | 295,101 (39.7%) |

The released post-ID corpus contains 938,961 posts in total.
Posts were identified through the TikTok Research API and can be hydrated with the included scraping code to retrieve currently available multimodal content and metadata from TikTok.

The federal-election release excludes posts outside the well-covered publication window and posts that only matched false-positive blacklisted keywords.
Random-sample subsets are not released.

## Files

- `data/saxony_2024/post_ids.parquet`: Saxony 2024 post IDs.
- `data/federal_2025/post_ids.parquet`: Federal election 2025 post IDs.
- `data/saxony_2024/annotations.parquet`: Human annotations for a Saxony-only subset.
- `hydrate.py`: Hydration script for recollecting currently available post media and metadata.

The post-ID files contain these columns:

- `post_id`: TikTok post ID, stored as a string.
- `collection`: Collection identifier (`saxony_2024` or `federal_2025`).
- `availability_YYYY_MM_DD`: Observed public availability at a re-scrape date.
- `status_codes_YYYY_MM_DD`: Pipe-separated TikTok status codes for posts marked `DELETED` in the matching availability column. Empty otherwise.

Availability values are:

| Value | Meaning |
|---|---|
| `AVAILABLE` | The post was successfully re-scraped and was publicly retrievable at that date. |
| `DELETED` | The post was not publicly retrievable and TikTok returned a durable unavailable, private, or moderation status. |
| `UNKNOWN_ERROR` | The re-scrape was attempted, but failed with a transient or inconclusive error, such as a WAF block, HTTP block, timeout, or parsing failure. |
| `NOT_RESCRAPED` | This post was not part of that re-scrape wave. |

The Saxony collection has availability snapshots for 2024-10-02, 2024-12-10, and 2025-01-13.
The federal-election collection has an availability snapshot for 2026-06-11.
Each post-ID file is exposed as a separate Hugging Face config, so each collection keeps only the availability columns that apply to it.

## Loading With Hugging Face Datasets

Install the Hugging Face datasets library:

```shell
pip install datasets
```

Load the Saxony 2024 post-ID release:

```python
from datasets import load_dataset

saxony_ids = load_dataset("tomasruiz/PoliTok-DE", "saxony_2024_post_ids")
saxony_ids = saxony_ids["train"]
```

Load the federal-election 2025 post-ID release:

```python
from datasets import load_dataset

federal_ids = load_dataset("tomasruiz/PoliTok-DE", "federal_2025_post_ids")
federal_ids = federal_ids["train"]
```

Load the Saxony human annotations:

```python
from datasets import load_dataset

annotations = load_dataset("tomasruiz/PoliTok-DE", "saxony_2024_annotations")
saxony_annotations = annotations["train"]
```

## Hydration Code

The script `hydrate.py` downloads currently available TikTok content from one post-ID parquet file.
It creates:

1. A video or image and audio file in the `media/` directory.
2. An entry in `media_progress.csv`, stating whether the post was successfully scraped.
3. An entry with post metadata in `media_metadata.csv`, only if the post was successfully scraped.

Install dependencies:

```shell
pip install -r requirements.txt
```

Hydrate the Saxony 2024 collection:

```shell
python hydrate.py --post-ids-file data/saxony_2024/post_ids.parquet --output-dir saxony_hydration
```

Hydrate the federal-election 2025 collection:

```shell
python hydrate.py --post-ids-file data/federal_2025/post_ids.parquet --output-dir federal_hydration
```

Note: To interrupt the script, you might need to press `Ctrl+C` multiple times due to the concurrent scraping code.

## Dataset Access

This repository contains post IDs and Saxony annotations.
It does not publicly release raw videos, images, audio, or full metadata.
Full content can be hydrated from TikTok when the post is still publicly available.
Access to stored deleted content is restricted and can be requested for academic research purposes.

## Citation

```bibtex
@article{ruiz2025politok,
  title={PoliTok-DE: A Multimodal Dataset of Political TikToks and Deletions From Germany},
  author={Ruiz, Tomas and Nanz, Andreas and Schmid, Ursula Kristin and Schwemmer, Carsten and Theocharis, Yannis and Rieger, Diana},
  journal={arXiv preprint arXiv:2509.15860},
  year={2025}
}
```
