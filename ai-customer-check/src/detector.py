from ultralytics import YOLO

class CustomerDetector:
    def __init__(self, model_path:str):
        self.model = YOLO(model_path)
    
    def detect(self,frame):
        results = self.model(frame,verbose=False)
        return results[0]