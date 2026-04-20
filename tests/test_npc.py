"""Tests for NPC shop: purchase, coin deduction, insufficient funds."""
from game.npc import sell_item, get_shop_sell_price, _load_npcs
from game.state import create_game_state


def _fresh_state(coins=10):
    s = create_game_state("Test", "classic")
    s["coins"] = coins
    return s


class TestNPC:
    def test_sell_item_not_owned(self):
        s = _fresh_state()
        s["inventory"].pop("healing_herb", None)
        result = sell_item(s, "healing_herb")
        assert "don't have" in result.lower()

    def test_sell_removes_item_at_zero(self):
        s = _fresh_state()
        s["inventory"]["capture_charm"] = 1
        sell_item(s, "capture_charm")
        assert "capture_charm" not in s["inventory"]

    def test_sell_item_adds_coins(self):
        s = _fresh_state()
        s["inventory"]["healing_herb"] = 3
        coins_before = s["coins"]
        # Mock the NPC data so sell price is known
        import game.npc as npc_mod
        original = npc_mod._get_npc_by_id
        npc_mod._get_npc_by_id = lambda name: {"shop": {"healing_herb": {"price": 6, "name": "Healing Herb"}}} if name == "Torv" else None
        try:
            result = sell_item(s, "healing_herb")
            assert s["inventory"]["healing_herb"] == 2
            assert s["coins"] == coins_before + 3  # 50% of 6
        finally:
            npc_mod._get_npc_by_id = original

    def test_get_sell_price_with_mock(self):
        import game.npc as npc_mod
        original = npc_mod._get_npc_by_id
        npc_mod._get_npc_by_id = lambda name: {"shop": {"healing_herb": {"price": 10}}} if name == "Torv" else None
        try:
            assert get_shop_sell_price("healing_herb") == 5
        finally:
            npc_mod._get_npc_by_id = original

    def test_get_sell_price_unknown_item(self):
        import game.npc as npc_mod
        original = npc_mod._get_npc_by_id
        npc_mod._get_npc_by_id = lambda name: {"shop": {}} if name == "Torv" else None
        try:
            assert get_shop_sell_price("unknown_item") == 1  # min 1 coin
        finally:
            npc_mod._get_npc_by_id = original
