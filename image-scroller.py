#!/usr/bin/env python
import time
from samplebase import SampleBase
from PIL import Image
from rgbmatrix import graphics

class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="../../../examples-api-use/runtext.ppm")
	self.parser.add_argument("-t", "--text", help="Text to display", default="Happy Halloween!")
	
    def run(self):
        if not 'image' in self.__dict__:
            self.image = Image.open(self.args.image).convert('RGB')
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

        double_buffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = self.image.size

	# Text
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/10x20.bdf")
        textColor = graphics.Color(255, 165, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text
	mytext = "%s" % (my_text)
	ssize = len(mytext)

        # let's scroll
        xpos = 0
        while xpos < img_width:
            xpos += 1
            if (xpos > img_width):
                xpos = 0
		exit

            double_buffer.SetImage(self.image, -xpos)
            double_buffer.SetImage(self.image, -xpos + img_width)

            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(0.1)


	counter = 0
	while counter < ((10 * ssize) + 20): 
            offscreen_canvas.Clear()
            length = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, my_text)
            pos -= 1
            if (pos + length < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)	
            counter += 1


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
