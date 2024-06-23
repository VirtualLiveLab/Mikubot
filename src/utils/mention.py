class MentionHelper:
    @staticmethod
    def get_user_mention(user_id: int) -> str:
        return f"<@{user_id}>"

    @staticmethod
    def get_role_mention(role_id: int) -> str:
        return f"<@&{role_id}>"

    @staticmethod
    def get_channel_mention(channel_id: int) -> str:
        return f"<#{channel_id}>"

    @staticmethod
    def get_voice_channel_mention(channel_id: int) -> str:
        return f"<#!{channel_id}>"
