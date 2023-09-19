from typing import Literal

from discord import Interaction, TextStyle, ui
from pydantic import BaseModel, Field

from components.ui.type import ModalCallback


class TextInput(BaseModel):
    label: str
    style: TextStyle = Field(default=TextStyle.short)
    placeholder: str | None = Field(default=None)
    default: str | None = Field(default=None)
    required: bool = Field(default=False)
    custom_id: str | None = Field(default=None)
    min_length: int | None = Field(default=None)
    max_length: int | None = Field(default=None)
    row: Literal[0, 1, 2, 3, 4] = Field(default=0)
    value: str = Field(default="")


class ModalOption(BaseModel):
    title: str = Field(min_length=1, max_length=45)
    inputs: list[TextInput] = Field(default=[])


class Modal(ui.Modal):
    def __init__(
        self,
        *,
        option: ModalOption,
        timeout: float | None = None,
        custom_id: str | None = None,
        on_submit: ModalCallback | None = None,
    ) -> None:
        __d = {
            "title": option.title,
            "timeout": timeout,
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_submit
        self.__inputs = option.inputs
        super().__init__(**__d)
        for _in in self.__inputs:
            __input_d = {
                "label": _in.label,
                "style": _in.style,
                "placeholder": _in.placeholder,
                "default": _in.default,
                "required": _in.required,
                "min_length": _in.min_length,
                "max_length": _in.max_length,
                "row": _in.row,
            }
            if _in.custom_id:
                __input_d["custom_id"] = _in.custom_id
            self.add_item(ui.TextInput(**__input_d))
            del __input_d

    async def on_submit(self, interaction: Interaction) -> None:
        if self.__callback_fn:
            await self.__callback_fn(interaction, {i.label: i.value for i in self.__inputs})
