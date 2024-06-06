from dataclasses import dataclass


@dataclass
class NewsData:
    category = str
    summary = str
    img_url = str
    link = str
    datetime = str
