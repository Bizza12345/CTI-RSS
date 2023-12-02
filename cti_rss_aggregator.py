import feedparser
import subprocess
import os

from xml.dom.minidom import Document

# List of RSS feed URLs
feeds = [
    "https://digital.nhs.uk/feed/cyber-alerts-feed.xml",
    "https://www.cisa.gov/cybersecurity-advisories/all.xml",
    "https://www.cyber.gov.au/rss/alerts",
    "https://www.cyber.gov.au/rss/advisories",
    "https://www.cyber.gov.au/rss/publications",
    "https://www.cyber.gov.au/rss/threats"
    # ... other feed URLs ...
]

# Create a new XML document
doc = Document()
rss = doc.createElement("rss")
rss.setAttribute("version", "2.0")
doc.appendChild(rss)

channel = doc.createElement("channel")
rss.appendChild(channel)

# Add custom channel details
title = doc.createElement("title")
title.appendChild(doc.createTextNode("Combined Cybersecurity Feed"))
channel.appendChild(title)

link = doc.createElement("link")
link.appendChild(doc.createTextNode("https://github.com/Bizza12345/CTI-RSS"))
channel.appendChild(link)

description = doc.createElement("description")
description.appendChild(doc.createTextNode("A combined feed of various cybersecurity RSS feeds"))
channel.appendChild(description)

# Aggregate entries from each feed
for url in feeds:
    d = feedparser.parse(url)
    for entry in d.entries:
        item = doc.createElement("item")

        # Add title for each item
        item_title = doc.createElement("title")
        item_title.appendChild(doc.createTextNode(entry.title))
        item.appendChild(item_title)

        # Add link for each item
        item_link = doc.createElement("link")
        item_link.appendChild(doc.createTextNode(entry.link))
        item.appendChild(item_link)

        # Add description for each item if available
        if hasattr(entry, 'description'):
            item_description = doc.createElement("description")
            item_description.appendChild(doc.createTextNode(entry.description))
            item.appendChild(item_description)

        channel.appendChild(item)

# Save the document to a file
with open("combined_feed.xml", "w") as f:
    f.write(doc.toprettyxml(indent="  "))

# Navigate to your repo's directory using a relative path or environment variable
os.chdir(os.environ.get('CTI-RSS_RepoPath', '.'))

# Git commands to add, commit, and push
subprocess.run(["git", "add", "combined_feed.xml"], shell=True)
subprocess.run(["git", "commit", "-m", "Updated RSS feed"], shell=True)
subprocess.run(["git", "push"], shell=True)