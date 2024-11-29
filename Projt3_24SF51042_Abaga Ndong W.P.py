import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("/content/wafer.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Border detection
edges = cv2.Canny(gray_blurred, 50, 150)


edges = cv2.Canny(gray_blurred, 210, 300)


#  line Detection   
lines = cv2.HoughLines(edges, 1.5, np.pi / 90, 180)  

filtered_lines = []
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * a)
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * a)


    if 100 < y1 < 300 or 400 < y1 < 600:
        filtered_lines.append(((x1, y1), (x2, y2)))
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


filtered_lines = sorted(filtered_lines, key=lambda line: line[0][1])
upper_line = filtered_lines[0]
lower_line = filtered_lines[-1]

# Calculate the central line
center_line = (
    ((upper_line[0][0] + lower_line[0][0]) // 2, (upper_line[0][1] + lower_line[0][1]) // 2),
    ((upper_line[1][0] + lower_line[1][0]) // 2, (upper_line[1][1] + lower_line[1][1]) // 2),
)
cv2.line(image, center_line[0], center_line[1], (0, 0, 255), 2)

# Calculate   the angle
delta_x = center_line[1][0] - center_line[0][0]
delta_y = center_line[1][1] - center_line[0][1]
theta = np.arctan2(delta_y, delta_x) * 180 / np.pi
print(f"Angle θ: {theta:.2f}°")


# Display the image with the detected lines and angle
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title(f"Angle: {theta:.2f}°")
plt.show()