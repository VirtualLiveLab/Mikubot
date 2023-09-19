from typing import Literal, TypedDict

from discord import Emoji, Interaction, PartialEmoji, ui
from discord import SelectOption as _SelectOption
from discord.enums import ChannelType
from pydantic import BaseModel, ConfigDict, Field

from components.ui.type import (
    ChannelSelectCallback,
    MentionableSelectCallback,
    RoleSelectCallback,
    SelectCallback,
    UserSelectCallback,
)
from components.ui.utils.call import call_any_function


class SelectStyle(TypedDict, total=False):
    disabled: bool
    placeholder: str | None
    row: Literal[0, 1, 2, 3, 4]


class SelectOption(BaseModel):
    label: str = Field(min_length=1, max_length=100)
    value: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=100)
    emoji: str | Emoji | PartialEmoji | None = Field(default=None)
    selected_by_default: bool = Field(default=False)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SelectConfigBase(TypedDict, total=False):
    min_values: int | None
    max_values: int | None


class SelectConfig(SelectConfigBase):
    options: list[SelectOption]


class ChannelSelectConfig(SelectConfigBase):
    channel_types: list[ChannelType]


class RoleSelectConfig(SelectConfigBase):
    pass


class MentionableSelectConfig(SelectConfigBase):
    pass


class UserSelectConfig(SelectConfigBase):
    pass


class Select(ui.Select):
    def __init__(
        self,
        *,
        config: SelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: SelectCallback | None = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
            "options": [
                _SelectOption(
                    label=option.label,
                    value=option.value or option.label,
                    description=option.description,
                    emoji=option.emoji,
                    default=option.selected_by_default,
                )
                for option in config["options"]
            ],
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: Interaction) -> None:
        if self.__callback_fn:
            await call_any_function(self.__callback_fn, interaction, self.values)


class ChannelSelect(ui.ChannelSelect):
    def __init__(
        self,
        *,
        config: ChannelSelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: ChannelSelectCallback | None = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
            "channel_types": config["channel_types"],
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: Interaction) -> None:
        if self.__callback_fn:
            await call_any_function(self.__callback_fn, interaction, self.values)


class RoleSelect(ui.RoleSelect):
    def __init__(
        self,
        *,
        config: RoleSelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: RoleSelectCallback | None = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: Interaction) -> None:
        if self.__callback_fn:
            await call_any_function(self.__callback_fn, interaction, self.values)


class MentionableSelect(ui.MentionableSelect):
    def __init__(
        self,
        *,
        config: MentionableSelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: MentionableSelectCallback | None = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: Interaction) -> None:
        if self.__callback_fn:
            await call_any_function(self.__callback_fn, interaction, self.values)


class UserSelect(ui.UserSelect):
    def __init__(
        self,
        *,
        config: UserSelectConfig,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: UserSelectCallback | None = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": config.get("min_values", None),
            "max_values": config.get("max_values", None),
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: Interaction) -> None:
        if self.__callback_fn:
            await call_any_function(self.__callback_fn, interaction, self.values)
