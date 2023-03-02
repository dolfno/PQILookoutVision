"""methods to manipulate the image"""
import cv2
# Add response text over image with confidence score
# def add_text_overlay(img, text:str, response):
#     """If anomaly show text in red otherwise in green"""
#     anomaly = response['DetectAnomalyResult']['IsAnomalous']
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     org = (50, 50)
#     fontScale = 1
#     # Blue color in BGR
#     color = (255, 0, 0)
#     thickness = 2
#     image = cv2.putText(img, 'OpenCV', org, font,
#                         fontScale, color, thickness, cv2.LINE_AA)
#     if anomaly:
#         #text red
#         cv2.putText(img, "Anomaly", (x, y), cv2.CV_FONT_HERSHEY_SIMPLEX, 2, 255)
#     else:
#         #text green
#     return

def add_text_overlay(img, response):
    """If anomaly show text in red otherwise in green"""
    anomaly = response['DetectAnomalyResult']['IsAnomalous']
    confscore = response['DetectAnomalyResult']['Confidence']
    if anomaly:
        color = (0, 0, 255)
        text = "Anomaly Detected"
        score = "Confidence score: " + str("%.4f" % confscore)
    else:
        color = (0, 255, 0)
        text = "Perfect Bottle"
        score = "Confidence score: " + str("%.4f" % confscore)
    font = cv2.FONT_HERSHEY_PLAIN
    img_overlay = cv2.putText(img, text, (10, 30), font, 1.5, color, 2, cv2.LINE_AA)
    img_overlay = cv2.putText(img, score, (10, 100), font, 1.5, color, 2, cv2.LINE_AA)
    return img_overlay

