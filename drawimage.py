#!/usr/bin/env python

import glob
import time

from samplebase import SampleBase
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class DrawImage(SampleBase):
    def __init__(self, *args, **kwargs):
        super(DrawImage, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="../../../examples-api-use/runtext.ppm")
	self.parser.add_argument("-t", "--text", help="Text to display", default="Happy Halloween!")


    def draw(self, image):
	self.matrix.Clear()
        self.image = Image.open(image).convert('RGB')
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        self.matrix.SetImage(self.image.convert('RGB'))

    def drawText(self, text):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/10x20.bdf")
        textColor = graphics.Color(255, 165, 0)
        pos = offscreen_canvas.width

        len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, text)
	counter = len + pos

        while counter > 0: 
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, text)

            pos -= 1
	    counter -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


    def run(self):

	pumpkins = glob.glob("images/pumpkin*.ppm")

	while True:
            pumpkins = glob.glob("images/pumpkin*.ppm")
	    for img in pumpkins:
                try:
                    print("Press CTRL-C to stop.")

		    self.draw(img)
   	            counter = 0 
                    while counter < 10:
 		        counter += 1
                        time.sleep(0.5)
		    self.drawText("We have Skittles, M&Ms, Starburst, and Candy Bars")
                except KeyboardInterrupt:
                    sys.exit(0)


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = DrawImage()
    if (not image_scroller.process()):
        image_scroller.print_help()
