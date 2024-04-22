from typing import TYPE_CHECKING, Literal

from .embed import deprecated_embed, fix_embed, wip_embed

if TYPE_CHECKING:
    from discord import Interaction


async def command_unavailable_callback(
    interaction: "Interaction",
    /,
    *,
    ephemeral: bool = False,
    status: Literal["FIX", "WIP", "DEPRECATED"],
    deprecated_alternative: str = "",
) -> None:
    match status:
        case "DEPRECATED":
            e = deprecated_embed(deprecated_alternative)
        case "FIX":
            e = fix_embed()
        case "WIP":
            e = wip_embed()
    if interaction.response.is_done():
        await interaction.followup.send(embed=e, ephemeral=ephemeral)
        return

    await interaction.response.send_message(embed=e, ephemeral=ephemeral)
    return
