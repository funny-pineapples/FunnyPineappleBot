from tgen import TextGenerator

from shared.database import Message
from shared.instances import session


class Samples:
    samples: dict[int, TextGenerator]

    def __init__(self) -> None:
        self.samples = {}

    def get(self, chat_id: int) -> TextGenerator:
        if chat_id not in self.samples:
            with session() as s:
                samples = [
                    m.tuple()[0]
                    for m in s.query(Message.message)
                    .filter(Message.chat_id == chat_id)
                    .all()
                ]

            self.samples[chat_id] = TextGenerator.from_samples(samples)
        return self.samples[chat_id]

    def delete(self, chat_id: int) -> None:
        if chat_id in self.samples:
            self.samples.pop(chat_id)


samples = Samples()
