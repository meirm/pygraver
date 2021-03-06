from base_protocol import BaseProtocol
import PIL.ImageOps as imops
from PIL import Image

class V3Protocol(BaseProtocol):

    version = "v3"

    def up(self):
        self._transmit(b"\xFF\x03\x01\x00")

    def down(self):
        self._transmit(b"\xFF\x03\x02\x00")

    def left(self):
        self._transmit(b"\xFF\x03\x03\x00")

    def right(self):
        self._transmit(b"\xFF\x03\x04\x00")


    # Some funcs have to be overridden:
    def start(self, burn_time):
        self._set_burn_time(burn_time)
        self._transmit(b"\xFF\x01\x01\x00")

    def _set_burn_time(self, burn_time):
        "Receives burn_time as an integer between 1 and 240"
        if burn_time < 0x01 or burn_time > 0xF0:
            raise ValueError("Burn time out of range: [1 (0x01), 240 (0xF0)]")
        burn_bin = bytes(burn_time,)
        self._transmit(b"\xFF\x05"+ bytes((burn_time,)) + b"\x00") # Converts to byte

    def pause(self):
        self._transmit(b"\xFF\x01\x02\x00")

    def reset(self):
        self._transmit(b"\xFF\x04\x01\x00")

    def center(self):
        self._transmit(b"\xFF\x02\x01\x00")

    def preview(self):
        self._transmit(b"\xFF\x02\x02\x00")

    def erase(self):
        self._transmit(b"\xFF\x06\x01\x00")
        return 50

    def upload_image(self, image):
        im = imops.pad(imops.invert(image),
                       (self.image_width-self.image_border,
                        self.image_height-self.image_border))\
                  .convert("1")

        # Create image wrapper to correct corner deformation
        wrapper = Image.new("1", (self.image_width, self.image_height))
        wrapper.paste(im, (int(self.image_border/2),
                           int(self.image_border/2),
                           int(self.image_width - self.image_border / 2),
                           int(self.image_height - self.image_border / 2)))
        wrapper.show()

        imbytes = im.tobytes()
        self._transmit(wrapper.tobytes())
        return len(imbytes)

