from src.chandra_bot.response_handler import handle_response,get_card_data,search_cards,get_name, get_card_image,get_link,get_price
from scrython import ScryfallError
import pytest


class TestResponseHandler:

    def test_handle_response(self):
        pass

    def test_get_card_data(self):
        card = get_card_data('Lightning Bolt')
        assert card.name() == 'Lightning Bolt'

    def test_get_card_data_no_card(self):
        card = get_card_data('Knedlicek')
        assert card == 'Error: No cards found matching “Knedlicek”'

    def test_get_card_data_exact(self):
        card = get_card_data('=Lightning Bolt')
        assert card.name() == 'Lightning Bolt'
    
    def test_get_card_data_exact_no_card(self):
        card = get_card_data('=Knedlicek')
        assert card == 'Error: No cards found matching “Knedlicek”'
    
    def test_get_card_data_no_name(self):
        card = get_card_data('')
        assert card == 'Error: string index out of range'
    
    def test_get_card_data_no_name_exact(self):
        card = get_card_data('=') 
        assert card == 'Error: You must provide a `fuzzy` or `exact` parameter'

    def test_search_cards(self):
        cards = search_cards('Lightning Bolt')
        assert len(cards) == 2
        assert cards[0] == 1
        assert cards[1][0][0] == 'Lightning Bolt'

    def test_search_cards_no_data(self):
        with pytest.raises(ScryfallError):
            cards = search_cards('')

    def test_get_name(self):
        assert get_name(get_card_data('=Lightning Bolt')) == 'Lightning Bolt'
    
    def test_get_name_wrong_data(self):
        with pytest.raises(AttributeError):
            get_name('Lightning bolt')

    def test_get_card_image(self):
        assert type(get_card_image(get_card_data('=Lightning Bolt'))) == str
    
    def test_get_card_image_wrong_data(self):
        with pytest.raises(AttributeError):
            get_card_image('Lightning Bolt')

    def test_get_link(self):
        assert type(get_link(get_card_data('=Lightning Bolt'))) == str or type(get_link(get_card_data('=Lightning Bolt'))) == None

    def test_get_link_wrong_data(self):
        assert get_link('Lightning bolt') == None
    
    def test_get_price(self):
        assert type(get_price(get_card_data('=Lightning Bolt'))) == list
        assert len(get_price(get_card_data('=Lightning Bolt'))) == 6
    
    def test_get_price_wrong_data(self):
        with pytest.raises(AttributeError):
            get_price('')
        
    