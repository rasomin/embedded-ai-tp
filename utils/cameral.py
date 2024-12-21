import cv2

def getCenterX(frame, left=False, right=False):
    if left:
        crop_img = frame[480:720, 270:660]
    elif right:
        crop_img = frame[480:720, 620:970]
    else:
        crop_img = frame[480:720, 445:835]
        
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    
    ret, thresh1 = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY)
    
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        return cx
    else:
        return False

def recognize_pt(frame, model):
    results = model(frame, verbose=False)
    return results[0].boxes.cls.to('cpu').tolist()