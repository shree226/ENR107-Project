from ultralytics import YOLO


model = YOLO("yolov8n.pt")


results = model.train(
    data="/workspaces/ENR107-Project/dataset/dataset.yaml", 
    epochs=50,         
    batch=8,           
    imgsz=256,         
    device="cpu",      
    workers=2,         
    amp=False,         
    plots=False,       
    cache=False        
)

model.export(format="torchscript", model="/workspaces/ENR107-Project/torchscript_model.pt")
