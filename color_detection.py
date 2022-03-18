import cv2
import pandas as pd
# to stores image path and csv path
img_path = 'pic2.jpg'
csv_path = 'colors.csv'

# reading csv file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# reading image
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600)) # Resizing the image

# declaring global variables
clicked = False
r = g = b = x_pos = y_pos = 0


# function to get the colour name from the csv file
def colour_name(R, G, B):
    minimum = 1000
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            colour_name = df.loc[i, 'color_name']

    return colour_name


# function to get RGB value of the coordinates clicked
def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# creating window
cv2.namedWindow('COLOUR DETECTION')
cv2.setMouseCallback('COLOUR DETECTION', draw_function)

while True:
    cv2.imshow('COLOUR DETECTION', img)
    if clicked:
        # creates a rectangle to display the colour
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)

        # creates the text to be written in the rectangle
        text = colour_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        # puts the text in the rectangle in white colour
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # puts the text in the rectangle in black colour if the colour of the rectangle is light
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(28) & 0xFF == 27:
        break

cv2.destroyAllWindows()
