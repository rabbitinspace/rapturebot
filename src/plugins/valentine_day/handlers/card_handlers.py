import textwrap
from typing import Optional, cast

import telegram

from src.plugins.valentine_day.helpers.helpers import get_reply_markup, get_username_or_link
from src.plugins.valentine_day.model import Card, CACHE_PREFIX
from src.utils.cache import cache, TWO_DAYS

HTML = telegram.ParseMode.HTML


class Store:
    def __init__(self, query: telegram.CallbackQuery):
        self.query = query
        self.message: telegram.Message = query.message
        self.user_id: int = query.from_user.id
        self.chat_id = self.message.chat_id
        self.message_id: int = self.message.message_id
        self.card: Optional[Card] = None

    def load(self) -> bool:
        """
        Загружает карточку из редиса и возвращает True, если она существует
        """
        self.card = cache.get(self._card_key())
        if self.card is None:
            self.query.answer('Закончилась Луна-красотка')
            return False
        return True

    def save(self) -> None:
        if self.card is None:
            raise TypeError('Card should be defined')
        cache.set(self._card_key(), self.card, time=TWO_DAYS)

    def is_already_clicked(self, button_name: str) -> bool:
        return cache.get(self._already_clicked_key(button_name), False)

    def mark_as_already_clicked(self, button_name: str) -> None:
        cache.set(self._already_clicked_key(button_name), True, time=TWO_DAYS)

    def update_buttons(self) -> None:
        if self.card is None:
            raise TypeError('Card should be defined')
        try:
            reply_markup = get_reply_markup(self.card.get_message_buttons())
            self.query.edit_message_reply_markup(reply_markup=reply_markup)
        except Exception:
            pass

    def _already_clicked_key(self, button_name: str) -> str:
        return f'{self._card_key()}:{button_name}:{self.user_id}'

    def _card_key(self) -> str:
        return f'{CACHE_PREFIX}:card:{self.chat_id}:{self.message_id}'


def revn_button_click_handler(_: telegram.Bot, __: telegram.Update,
                              query: telegram.CallbackQuery, ___) -> None:
    """
    Обработчик кнопки ревности
    """
    store = Store(query)
    if not store.load():
        return
    store.card = cast(Card, store.card)

    button_name = 'revn_clicked'
    result = store.card.revn(store.user_id, store.is_already_clicked(button_name))

    if result.success:
        store.mark_as_already_clicked(button_name)
        store.save()
        store.update_buttons()
    query.answer(result.text)


def mig_button_click_handler(bot: telegram.Bot, _: telegram.Update,
                             query: telegram.CallbackQuery, __) -> None:
    """
    Обработчик кнопки подмигивания
    """
    store = Store(query)
    if not store.load():
        return
    store.card = cast(Card, store.card)

    button_name = 'mig_clicked'
    result = store.card.mig(store.user_id, store.is_already_clicked(button_name),
                            get_username_or_link(store.user_id))

    query.answer(result.text)
    if result.success:
        store.mark_as_already_clicked(button_name)
        try:
            bot.send_message(store.card.from_user.user_id, result.notify_text, parse_mode=HTML)
        except Exception:
            pass


def about_button_click_handler(bot: telegram.Bot, _: telegram.Update,
                               query: telegram.CallbackQuery, __) -> None:
    text = textwrap.dedent(
        """
        Сегодня 14 февраля. Все отправляют валентинки! 

        Тоже хотите? Напишите /help боту в личку.
        """).strip()
    bot.answer_callback_query(query.id, text, show_alert=True)
