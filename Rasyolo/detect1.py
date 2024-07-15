from Rasyolo.getDistance import GetDistance
def run(model, image, save, conf_thres):
    results = model.predict(source=image, save=save)
    boxes = results[0].boxes.xyxy.cpu().tolist()
    clss = results[0].boxes.cls.cpu().tolist()
    confi = results[0].boxes.conf.cpu().tolist()
    decision = (0,0,0,0,'')
    for box, cls, conf in zip(boxes, clss, confi):
        if conf >= conf_thres:
            bbox_center = ((box[0]+box[2])/2, (box[1]+box[3])/2)
            cls = model.model.names[int(cls)]
            decision = GetDistance(bbox_center)
    return decision
