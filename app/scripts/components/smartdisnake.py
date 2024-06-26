from disnake.ui import Modal, TextInput
from disnake import Embed, TextInputStyle


class SmartModal(Modal):
    def __init__(self, modal_cfg: dict):
        self.modal_cfg = modal_cfg
        super().__init__(title=modal_cfg["title"],
                         custom_id=modal_cfg["custom_id"],
                         components=[
                            TextInput(
                                label=ti["label"],
                                placeholder=ti["placeholder"],
                                max_length=ti["max_length"],
                                min_length=ti["min_length"],
                                required=ti["required"],
                                custom_id=ti["custom_id"],
                                style=TextInputStyle.long if ti["style"] == "long" else TextInputStyle.short
                            ) for ti in modal_cfg["text_inputs"]
                        ]
                         )


'''

{
    "part": int,
    "title": "str",
    "phrase_req_words": "Братик, напиши пожалуйста от {min_words} слов"
    "fields" :
    {         
            "question": "str 45 characters",
            "data_type": "str/int/(custom)",
            "custom_id": "str",
            "style": "long / short *optional"
            "min_words": "int *optional"
    }

}
            
'''


class SmartRegModal(Modal):
    def __init__(self, modal_cfg: dict):
        self.modal_cfg = modal_cfg
        super().__init__(
            title=self.modal_cfg["title"].format(part=int(modal_cfg["part"])),
            # custom_id=modal_cfg["custom_id"],
            components=[
                TextInput(
                    label=field["question"],
                    placeholder=self.__get_placeholder(field),
                    max_length=3999,
                    min_length=0,
                    required=True,
                    custom_id=field["custom_id"],
                    style=TextInputStyle.long if field.get("style") == "long" else TextInputStyle.short
                ) for field in modal_cfg["fields"]
            ]

        )

    def __get_placeholder(self, field: dict) -> str:
        placeholder = "-"
        if not field.get("example") is None:
            return field["example"]
        if not field.get("min_words") is None:
            return self.modal_cfg["phrase_req_words"].format(min_words=field["min_words"])
        return placeholder



class SmartEmbed(Embed):
    def __init__(self, cfg: dict, **kwargs):
        super().__init__(
            title=cfg.get("title"),
            description=cfg.get("c"),
            **kwargs
        )
        for field in cfg["fields"]:
            super().add_field(
                name=field["name"],
                value=field["value"],
                inline=field["inline"],
            )