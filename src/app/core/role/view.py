from discord import Embed, Interaction, Role
from ductile import State, View, ViewObject
from ductile.ui import Button, RoleSelect

from src.const.discord import MAX_EMBED_FIELD_VALUE_LENGTH
from src.const.enums import Color


class RoleCheckView(View):
    def __init__(self) -> None:
        super().__init__()
        self.selected = State[Role | None](None, self)

    def render(self) -> ViewObject:
        async def handle_select(interaction: Interaction, values: list[Role]) -> None:
            await interaction.response.defer()
            self.selected.set_state(values[0])

        def default_embed() -> Embed:
            return Embed(
                title="ロール概要",
                description="見たいロールを選択してください。",
                color=Color.MIKU,
            )

        def role_embed(role: Role) -> Embed:
            value = "\n".join([m.mention for m in role.members])
            if len(value) > MAX_EMBED_FIELD_VALUE_LENGTH:
                value = f"{value[: MAX_EMBED_FIELD_VALUE_LENGTH - 3]}..."

            e = Embed(
                title="ロール概要",
                description=f"{role.mention}の概要を表示しています。",
                color=Color.MIKU,
            )
            e.add_field(
                name=f"このロールを持つメンバー({len(role.members)}人)",
                value=value,
            )
            return e

        return ViewObject(
            embeds=[default_embed() if (r := self.selected()) is None else role_embed(r)],
            components=[
                RoleSelect(
                    config={"min_values": 1, "max_values": 1},
                    style={
                        "placeholder": "確認したいロールを選択してください。",
                    },
                    on_select=handle_select,
                ),
            ],
        )


class AndMentionView(View):
    def __init__(self) -> None:
        super().__init__()
        self.disabled = State[bool](False, self)  # noqa: FBT003
        self.selected = State[list[Role]]([], self)

    def render(self) -> ViewObject:
        default_embed = Embed(
            title="ANDメンション",
            description="指定された複数のロールをすべて持っているメンバーをメンションします。",
            color=Color.MIKU,
        )

        async def handle_select(interaction: Interaction, values: list[Role]) -> None:
            await interaction.response.defer()
            self.selected.set_state(values)

        async def stop_view(interaction: Interaction) -> None:
            await interaction.response.defer()
            self.disabled.set_state(True)
            self.stop()

        def role_embed(roles: list[Role]) -> Embed:
            e = Embed(
                title="ANDメンション",
                description="以下のロールをすべて持っているメンバーをメンションします。",
                color=Color.MIKU,
            )
            e.add_field(
                name="対象ロール",
                value="\n".join([r.mention for r in roles]),
            )
            return e

        return ViewObject(
            embeds=[default_embed if (r := self.selected()) == [] else role_embed(r)],
            components=[
                RoleSelect(
                    config={"min_values": 1, "max_values": 5},
                    style={
                        "placeholder": "メンションしたいロールを選択してください。(最大5個まで)",
                        "row": 0,
                        "disabled": self.disabled(),
                    },
                    on_select=handle_select,
                ),
                Button(
                    "完了",
                    style={"color": "green", "row": 1, "disabled": self.disabled()},
                    on_click=stop_view,
                ),
            ],
        )
