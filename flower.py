from ultralytics import YOLO
import math
import pyautogui
import json


class Flower():
    def __init__(self):
        self.x = pyautogui.size()[0] / 2
        self.y = pyautogui.size()[1] / 2
        self.model = YOLO("best_yolo11n.pt") # Using nano model to be able to run on low end machines. It isn't very accurate though.

    def find_closest_enemy(self,results):
        closest_name = None
        closest_position = None
        closest_distance = 10000

        enemy_boxes = results[0].boxes
        for enemy_box in enemy_boxes:
            enemy_name = self.model.names[int(enemy_box.cls)]
            x,y,width,height = enemy_box.xywh[0]
            x,y,width,height = x.item(),y.item(),width.item(),height.item()
            distance = math.dist([x,y],[self.x,self.y])
            if distance < closest_distance:
                closest_name = enemy_name
                closest_position = {'x': x,'y':y,'width':width,'height':height}
                closest_distance = distance
            
        closest_enemy = {'position': closest_position,'name': closest_name, 'distance': closest_distance}

        return closest_enemy

    def choose_move(self,enemy):
        '''Decide whether to attack, run, or stay still'''
        if enemy["distance"] > 120:
            return "Attack"
        elif enemy["distance"] < 100:
            return "Run"
        else:
            return "Stay"

    def attack(self,enemy):
        # Move the cursor to the enemy's location and click
        pyautogui.moveTo(enemy["position"]["x"],enemy["position"]["y"])
        pyautogui.mouseDown()
    
    def run(self,enemy):
        # Move the cursor to the opposite direction of the enemy
        magnitude = 100
        x_pos = -math.copysign(magnitude,(enemy["position"]["x"] - self.x))
        y_pos = -math.copysign(magnitude,(enemy["position"]["y"] - self.y))
        pyautogui.moveTo(self.x + x_pos,self.y + y_pos)

    def stay(self):
        # Move the cursor on top of the players current position
        pyautogui.moveTo(self.x,self.y)

    def step(self):
        results = self.model.predict("test.jpg", imgsz=640, conf=0.8)
        closest_enemy = self.find_closest_enemy(results)

        if closest_enemy['name'] is not None:
            choice = self.choose_move(closest_enemy)
            if choice == 'Attack':
                self.attack(closest_enemy)
            elif choice == 'Run':
                self.run(closest_enemy)
            elif choice == 'Stay':
                self.stay()

        bounding_boxes = []
        enemy_boxes = results[0].boxes
        for enemy_box in enemy_boxes:
            enemy_name = self.model.names[int(enemy_box.cls)]
            x,y,width,height = enemy_box.xywh[0]
            bounding_box = [x.item(),y.item(),width.item(),height.item(),enemy_name]
            bounding_boxes.append(bounding_box)
    
        with open('enemy.json','w+') as file:
            json.dump(bounding_boxes,file)
