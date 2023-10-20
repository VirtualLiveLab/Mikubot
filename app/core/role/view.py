from discord import Embed, Interaction, Role, ui
from ductile import State, View, ViewObject
from ductile.ui import Button, RoleSelect

from const.enums import Color


class RoleCheckView(View):
    def __init__(self) -> None:
        super().__init__()
        self.selected = State[Role | None](None, self)
        self.current_page = State[int](0, self)
        self.max_page = 0

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
            # chunk role members by 20
            chunked_members = [role.members[i : i + 20] for i in range(0, len(role.members), 20)]
            self.max_page = len(chunked_members) - 1

            def get_page_value() -> str:
                return "\n".join([m.mention for m in chunked_members[self.current_page()]])

            e = Embed(
                title="ロール概要",
                description=f"{role.mention}の概要を表示しています。",
                color=Color.MIKU,
            )
            e.add_field(
                name=f"このロールを持つメンバー({self.current_page() + 1}/{len(chunked_members)})",
                value=get_page_value(),
            )
            return e

        components: list[ui.Item] = [
            RoleSelect(
                config={"min_values": 1, "max_values": 1},
                style={
                    "placeholder": "確認したいロールを選択してください。",
                },
                on_select=handle_select,
            ),
        ]
        if self.max_page > 1:
            components += [
                Button(
                    "<",
                    style={"color": "grey", "disabled": self.current_page() == 0},
                    on_click=lambda _: self.current_page.set_state(lambda x: x - 1),
                ),
                Button(
                    f"{self.current_page() + 1}/{self.max_page + 1}",
                    style={"color": "grey", "disabled": True},
                ),
                Button(
                    ">",
                    style={
                        "color": "grey",
                        "disabled": self.current_page() == self.max_page,
                    },
                    on_click=lambda _: self.current_page.set_state(lambda x: x + 1),
                ),
            ]

        return ViewObject(
            embeds=[default_embed() if (r := self.selected()) is None else role_embed(r)],
            components=components,
        )
