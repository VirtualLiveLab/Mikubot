from typing import TYPE_CHECKING, Literal

from .embed import fix_embed, wip_embed

if TYPE_CHECKING:
    from discord import Interaction


async def command_unavailable_callback(
    interaction: "Interaction",
    /,
    *,
    ephemeral: bool = False,
    status: Literal["FIX", "WIP"],
) -> None:
    e = wip_embed() if status == "WIP" else fix_embed()
    if interaction.response.is_done():
        await interaction.followup.send(embed=e, ephemeral=ephemeral)
        return

    await interaction.response.send_message(embed=e, ephemeral=ephemeral)
    return
