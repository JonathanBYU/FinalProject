import pytest
from flower import Flower
from pytest import approx


flower = Flower()

def test_find_closest_enemy():
    input = flower.model.predict("test_data/test1.png")
    assert type(flower.find_closest_enemy(input)) == dict
    assert flower.find_closest_enemy(input)["name"] == "Ladybug"
    assert flower.find_closest_enemy(input)["distance"] == approx(276,abs=5)
    assert flower.find_closest_enemy(input)["position"] == {'x': approx(780,abs=15),'y': approx(329,abs=15),'width': approx(32,abs=5),'height': approx(34,abs=5)}

def test_choose_move():
    enemy = {'position': {'x':300,'y': 400,'width': 30,'height': 30},'name': "Ladybug", 'distance': 100}
    enemy2 = {'position': {'x':300,'y': 400,'width': 30,'height': 30},'name': "Bee", 'distance': 220}
    enemy3 = {'position': {'x':300,'y': 400,'width': 30,'height': 30},'name': "Rock", 'distance': 80}
    assert type(flower.choose_move(enemy)) == str
    assert type(flower.choose_move(enemy2)) == str
    assert type(flower.choose_move(enemy3)) == str
    assert flower.choose_move(enemy) == "Stay"
    assert flower.choose_move(enemy2) == "Attack"
    assert flower.choose_move(enemy3) == "Run"
    

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
