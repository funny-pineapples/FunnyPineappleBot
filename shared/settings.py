from json import dump, load

from pydantic import BaseModel, BaseSettings, Field


class Settings(BaseSettings):
    token: str


class GenConfig(BaseModel):
    chance: int = Field(
        10,
        description="Шанс с которым бот сгенерирует сообщение",
        ge=1,
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
    min_word_count: int | str | None = Field(
        None,
        description="Минимальное количество слов в сгенерированном предложении",
        ge=1,
    )
    max_word_count: int | None = Field(
        None,
        description="Максимальное количество слов в сгенерированном предложении",
        ge=1,
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


class Chats(BaseModel):
    chats: dict[int, Config] = {}

    @classmethod
    def load(cls, file_name: str) -> "Chats":
        with open(file_name, "r") as file:
            return cls.parse_obj(load(file))

    def save(self, file_name: str) -> None:
        with open(file_name, "w") as file:
            dump(self.schema(), file)

    def get_config(self, chat_id: int) -> Config:
        if chat_id not in self.chats:
            self.chats[chat_id] = Config()
        return self.chats[chat_id]

    def set_config(self, chat_id: int, config: Config) -> None:
        self.chats[chat_id] = config
