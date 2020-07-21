#!/usr/bin/env python3
import feedparser
import pathlib
import os
import re

root = pathlib.Path(__file__).parent.resolve()

TOKEN = os.environ.get("GITHUB_TOKEN")
BLOG_URL = os.environ.get("MEDIUM_BLOG_URL")

def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def fetch_blog_entries():
    entries = feedparser.parse(BLOG_URL)["entries"]
    return [
            {
                "title": entry["title"],
                "url": entry["link"],
                "published": re.split(r"\W[0-9]{2}:[0-9]{2}:[0-9]{2}", entry["published"])[0]
            }
            for entry in entries 
            ]

if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()
    rewritten = ""
    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)

    print ("Writing: \n{}".format(rewritten))
    readme.open("w").write(rewritten)
