import discord

from src.const.enums import Color

from .processor import NotionPage


def process_notion_page_to_embeds(page: NotionPage) -> discord.Embed:
    e = discord.Embed(
        title=f"{page['emoji']} {page['title']}" if page["emoji"] else page["title"],
        url=page["url"],
        color=Color.MIKU,
        timestamp=page["last_updated"],
    )
    e.set_image(url=page["image"])
    e.set_footer(text="Created on Notion")
    return e
