from discord import Embed

from src.const.enums import Color


def wip_embed() -> Embed:
    return Embed(
        title="準備中",
        description="この機能は現在準備中です。もうちょっとまってね！",
        color=Color.MIKU,
    )


def fix_embed() -> Embed:
    return Embed(
        title="修正中",
        description="この機能は現在修正中です。もうちょっとまってね！",
        color=Color.MIKU,
    )


def deprecated_embed(alternative: str) -> Embed:
    return Embed(
        title="非推奨",
        description=f"この機能は非推奨になりました。\n代わりに{alternative}を使ってください。",
        color=Color.MIKU,
    )
