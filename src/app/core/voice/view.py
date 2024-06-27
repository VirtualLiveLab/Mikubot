from dataclasses import dataclass

from discord import Embed, VoiceChannel
from ductile import State, View
from ductile.view import ViewObject

from src.const.enums import Color, TaskStatus


@dataclass
class MaximizeBitrateTask:
    channel_mention: str
    status: TaskStatus = TaskStatus.PENDING

    def to_string(self) -> str:
        return f"{self.status} {self.channel_mention}"


class MaximizeBitrateView(View):
    def __init__(self, voice_channels: list[VoiceChannel]) -> None:
        super().__init__()
        self.embed_title = "ビットレート自動調整"
        self.tasks_amount = len(voice_channels)
        self.tasks = State[dict[int, MaximizeBitrateTask]](
            {vc.id: MaximizeBitrateTask(vc.mention) for vc in voice_channels},
            self,
        )

    def render(self) -> ViewObject:
        if self.tasks == {}:
            return ViewObject(
                embeds=[
                    Embed(
                        title=self.embed_title,
                        description="サーバー内にボイスチャットが見つかりませんでした。",
                    )
                ]
            )

        def get_tasks_string() -> str:
            return "\n".join([task.to_string() for task in self.tasks().values()])

        def embed_task() -> Embed:
            return Embed(
                title=self.embed_title,
                description=f"ボイスチャットが{self.tasks_amount}個見つかりました。\nビットレートを最大に調整しています。\n\n{get_tasks_string()}",
                color=Color.MIKU,
            )

        return ViewObject(embeds=[embed_task()])

    def set_task_state(self, channel_id: int, status: TaskStatus) -> None:
        def set_state(c: dict[int, MaximizeBitrateTask]) -> dict[int, MaximizeBitrateTask]:
            c[channel_id].status = status
            return c

        self.tasks.set_state(set_state)
