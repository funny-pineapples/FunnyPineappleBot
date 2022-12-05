from json import dump, load

from pydantic import BaseModel, BaseSettings, Field


class Settings(BaseSettings):
    token: str


class GenConfig(BaseModel):
    chance: int = Field(
        10,
        description="Шанс с которым бот сгенерирует сообщение",
        ge=0,
        le=100,
    )
    reply: bool = Field(
        True,
        description="Включить/Выключить ответ на сообщение",
    )
    delete_command: bool = Field(
        True,
        description="Включить/Выключить удаление /gen команды",
    )


class PollConfig(BaseModel):
    answer_count: int = Field(
        4,
        description="Минимальное количество голосов для проверки опроса",
    )
    anonym: bool = Field(
        False,
        description="Включить/Выключить анонимный опрос",
    )


class Config(BaseModel):
    gen: GenConfig = Field(
        GenConfig(),
        description="Настройки генерации сообщений",
    )
    pin: PollConfig = Field(
        PollConfig(),
        description="Настройки закрепления сообщений",
    )
    members: PollConfig = Field(
        PollConfig(),
        description="Настройки принятия людей в группу",
    )


class Chats:
    file_name: str
    configs: dict[int, Config]

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.configs = {}

    def load(self) -> None:
        with open(self.file_name, "r") as file:
            self.configs = {
                id_: Config.parse_obj(config) for id_, config in load(file).items()
            }

    def save(self) -> None:
        with open(self.file_name, "w") as file:
            dump({id_: config.dict() for id_, config in self.configs.items()}, file)

    def get(self, chat_id: int) -> Config:
        if chat_id not in self.configs:
            self.configs[chat_id] = Config()
        return self.configs[chat_id]

    def set(self, chat_id: int, config: Config) -> None:
        self.configs[chat_id] = config
        self.save()
