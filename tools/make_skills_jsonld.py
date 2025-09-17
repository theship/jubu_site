#!/usr/bin/env python3
"""
Generate JSON-LD from skills_vocab.csv

Inputs (default):
  CSV:   {REPO_ROOT}/docs/ai/skills_vocab.csv

Outputs (default):
  JSON:  {REPO_ROOT}/docs/ai/skills.jsonld
         {REPO_ROOT}/docs/ai/skills_defined_terms.jsonld

Public URLs (default):
  SITE_ROOT: https://juleeburdekin.com
  /ai/skills_vocab.csv, /ai/skills.jsonld, /ai/skills_defined_terms.jsonld

Override with CLI flags:
  --ai-dir           local folder for CSV + JSON-LD (default: docs/ai)
  --site-root        public site root (default: https://juleeburdekin.com)
  --public-ai-path   public path where AI assets are served (default: /ai/)
  --resume-url       public resume URL (default: https://juleeburdekin.com/resume/)
"""

import json
import argparse
import pandas as pd
from datetime import date
from pathlib import Path

def parse_args():
    repo_root = Path(__file__).resolve().parents[1]
    return argparse.Namespace(**{
        "ai_dir": repo_root / "docs" / "ai",
        "site_root": "https://juleeburdekin.com",
        "public_ai_path": "/ai/",
        "resume_url": "https://juleeburdekin.com/resume/"
    })

def parse_cli():
    parser = argparse.ArgumentParser()
    repo_root = Path(__file__).resolve().parents[1]
    parser.add_argument("--ai-dir", type=Path, default=repo_root / "docs" / "ai")
    parser.add_argument("--site-root", type=str, default="https://juleeburdekin.com")
    parser.add_argument("--public-ai-path", type=str, default="/ai/")
    parser.add_argument("--resume-url", type=str, default="https://juleeburdekin.com/resume/")
    return parser.parse_args()

def main():
    args = parse_cli()

    # Normalize public path (ensure leading/trailing slash)
    pub_ai = "/" + args.public_ai_path.strip("/") + "/"

    # Local paths
    ai_dir: Path = args.ai_dir
    ai_dir.mkdir(parents=True, exist_ok=True)

    csv_path = ai_dir / "skills_vocab.csv"
    out_person = ai_dir / "skills.jsonld"
    out_termset = ai_dir / "skills_defined_terms.jsonld"

    if not csv_path.exists():
        raise SystemExit(f"Missing CSV: {csv_path}\n"
                         f"Place your canonical skills_vocab.csv there or pass --ai-dir to the script.")

    # Public URLs (what crawlers will hit post-deploy)
    csv_url = f"{args.site_root.rstrip('/')}{pub_ai}skills_vocab.csv"
    person_url = f"{args.site_root.rstrip('/')}{pub_ai}skills.jsonld"
    termset_url = f"{args.site_root.rstrip('/')}{pub_ai}skills_defined_terms.jsonld"

    df = pd.read_csv(csv_path)

    # ---- Person JSON-LD ----
    # Build knowsAbout as a SET from categories + tags, then convert to a sorted LIST
    know_tags = set()
    for tags in df.get("tags", pd.Series(dtype=str)).fillna(""):
        for t in str(tags).split("|"):
            t = t.strip()
            if t:
                know_tags.add(t)

    knows_about = sorted(set(df["category"].dropna().unique().tolist()) | know_tags)

    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Julee Burdekin",
        "url": args.site_root.rstrip("/") + "/",
        "mainEntityOfPage": args.resume_url,
        "sameAs": [
            "https://www.linkedin.com/in/jburdekin/",
            "https://github.com/theship/",
            "https://gnowledge-karden.ghost.io/"
        ],
        "subjectOf": [csv_url],
        "skills": sorted(df["skill"].dropna().unique().tolist()),
        "knowsAbout": knows_about    # <-- always an array
    }

    # ---- DefinedTermSet JSON-LD ----
    defined_terms = []
    for _, row in df.iterrows():
        props = []
        for name in ["category","aliases","tags","publicly_attested","conversation_derived","seniority","recency"]:
            if name in row and pd.notna(row[name]):
                props.append({"@type": "PropertyValue", "name": name, "value": str(row[name])})

        defined_terms.append({
            "@type": "DefinedTerm",
            "name": str(row["skill"]),
            "inDefinedTermSet": csv_url,
            "additionalProperty": props
        })

    termset = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "Julee Burdekin Skills Vocabulary",
        "url": csv_url,
        "dateModified": str(date.today()),
        "hasDefinedTerm": defined_terms
    }

    out_person.write_text(json.dumps(person, indent=2, ensure_ascii=False), encoding="utf-8")
    out_termset.write_text(json.dumps(termset, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote:\n  {out_person}\n  {out_termset}")
    print(f"Public URLs:\n  {csv_url}\n  {person_url}\n  {termset_url}")

if __name__ == "__main__":
    main()
