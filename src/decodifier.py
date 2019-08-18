class Decodifier:
    """
    Class used for steganographic encoding/decoding

    Methods
    -------
    encode(text)
        encodes text to an image
    decode()
        decodes text from an image
    """
    
    def __init__(self, img, color, nbits):
        """
        Parameters
        ----------
        img: ndarray
            an array of the pixels of an image
        color: bool
            if the image is in color
        nbits: int
            the amount of pixels for encoding/decoding
        """
        self._img = img
        self._color = color
        self._nbits = nbits
        self._encoding = "ASCII"
        self._cur = (0, 0, 0)


    def decode(self):
        """
        Returns the text from decoding the image 
        """
        bits = 0
        bitQ = 0
        mask = 2**self._nbits - 1
        text = []
        self._next()
        while self._hasNext():
            bits += 2**bitQ * self._extract(mask)
            bitQ += self._nbits
            self._next()
            if bitQ > 8:
                text.append(bits % 256)
                bits = int(bits/256)
                bitQ -= 8
                if text[-1] == 0:
                    return bytes(text[:-1]).decode(self._encoding)
        return bytes(text[:-1]).decode(self._encoding)
        

    def encode(self, text):
        """
        Returns the image with the encoded text

        Parameters
        ----------
        text: str
            the string to be encoded
        """
        txtbytes = bytearray(text, 'ASCII')
        txtbytes.append(0)
        finished = False
        dims = self._img.shape
        mask = 2**self._nbits - 1
        c = 0
        bits = 0
        bitQ = 0
        self._insert(self._nbits - 1, 7)
        self._next()
        while self._hasNext():
            if bitQ < self._nbits:
                try:
                    t = txtbytes[c]
                    bits += 2**bitQ * t
                    c += 1
                    bitQ += 8
                except:
                    finished = True
            self._insert(bits, mask)
            bits = int(bits / (mask + 1))
            bitQ -= self._nbits
            if finished:
                return self._img
            self._next()
        raise AttributeError("Not enough space for text. Try using more bits per pixel or a bigger image.")


    def _next(self):
        x, y, z = self._cur 
        if self._color:
            dims = self._img.shape
        else:
            dims = (self._img.shape[0], self._img.shape[1], 1)
        z += 1
        if z == dims[2]:
            y, z = y + 1, 0
            if y == dims[1]:
                x, y = x + 1, 0
        self._cur = (x, y, z)

    def _hasNext(self):
        return self._cur[0] < self._img.shape[0]

    def _insert(self, buffer, bitMask):
        x, y, z = self._cur
        if self._color:
            data = self._img[x][y][z]
        else:
            data = self._img[x][y]
        data = (data & (255 - bitMask)) + (bitMask & buffer)
        if self._color:
            self._img[x][y][z] = data
        else:
            self._img[x][y] = data
        
    def _extract(self, bitMask):
        x, y, z = self._cur
        if self._color:
            data = self._img[x][y][z]
        else:
            data = self._img[x][y]
        return data & bitMask