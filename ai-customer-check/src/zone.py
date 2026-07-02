import cv2

# Frame of the frontal shop
def draw_zone(frame,zone):
    x1,y1,x2,y2 = zone

    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
    cv2.putText(
        frame,
        "Customer Zone",
        (x1, y1-10),
        cv2.FONT_HERSHEY_COMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    return frame

# Middle point of person
def is_point_inside_zone(point, zone):
    px,py = point
    x1,y1,x2,y2 = zone

    return x1 <= px <= x2 and y1 <= py <= y2

# Box around person
def get_box_center(box):
    x1,y1,x2,y2 = box

    center_x = int((x1+x2)/2)
    center_y = int((y1+y2)/2)

    return center_x, center_y