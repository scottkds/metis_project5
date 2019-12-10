# This program allows the user to automatically save image segments. The image
# segments are 40x40

# imports
import argparse
import cv2
import os

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
glyph = 'glyphs'
save_path = None

def click_and_crop(event, x, y, flags, param):
	"""Selects a 40x40 window of the displayed image and automatically saves
	the image segement."""
	# grab references to the global variables
	global refPt, cropping, img_shape, glyph, save_path

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		print('Cropping at x = {}, y = {}'.format(x, y))
		# x_coord and y_coord are the cooordinates for the center point of the
		# image segement. If a boundry is detected the window is moved adjusted
		# to be totall within the image.
		x_coord = x - 20
		y_coord = y - 20
		if x_coord < 0:
			x_coord = 0
		if y_coord < 0:
			y_coord = 0
		x_end = x_coord + 40
		y_end = y_coord + 40
		if x_end > img_shape[1]:
			diff = x_end - img_shape[1]
			x_coord = x_coord - diff
			x_end = x_end - diff
		if y_end > img_shape[0]:
			diff = y_end - img_shape[0]
			y_coord = y_coord - diff
			y_end = y_end - diff
		refPt = [(x_coord, y_coord), (x_end, y_end)]
		cropping = True
		crop_img = image[y_coord:y_end, x_coord:x_end].copy()
		filename = 'img_x_{}_y_{}.png'.format(x, y)
		file = os.path.join(save_path, glyph, filename)
		print(file)
		cv2.imwrite(file, crop_img)
		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		cropping = False




# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-p", "--path", required=True, help="Path to save files")
ap.add_argument("-q", "--quarter", required=False, help="Quarter of the image to show counter clockwise")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])

# Get the image dimensions
height, width, depth = image.shape
print((height, width, depth))
half_width = width // 2
half_height = height // 2

# The quarters aprameter splits the image into 4ths so it is easier to see on
# the screen.
if args['quarter'] == '1':
	print(args['quarter'])
	image = image[:half_height, :half_width].copy()
elif args['quarter'] == '2':
	print(args['quarter'])
	image = image[:half_height, half_width:].copy()
elif args['quarter'] == '3':
	print(args['quarter'])
	image = image[half_height:, :half_width].copy()
elif args['quarter'] == '4':
	print(args['quarter'])
	image = image[half_height:, half_width:].copy()
else:
	pass

# Set up the save path if it doesn't already exist.
save_path = args['path']
if not os.path.exists(os.path.join(save_path, 'glyphs')):
	os.makedirs(os.path.join(save_path, 'glyphs'))
if not os.path.exists(os.path.join(save_path, 'non_glyphs')):
	os.makedirs(os.path.join(save_path, 'non_glyphs'))
img_shape = image.shape
print(img_shape)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow('image', image)
	key = cv2.waitKey(10) & 0xFF

	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()

	if key == ord('g'):
		glyph = 'glyphs'

	if key == ord('n'):
		glyph = 'non_glyphs'

	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	cv2.imshow("ROI", roi)
	cv2.waitKey(0)

# close all open windows
cv2.destroyAllWindows()
