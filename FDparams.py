class FDparams:
    def __init__(self, writeFile, scale, scaledHeight, scaledWidth, winWidth, winHeight, stepWidth, stepHeight, argsStr, pixelThreshold, drawBox):
        self.writeFile = writeFile
        self.scale = scale
        self.scaledHeight = scaledHeight
        self.scaledWidth = scaledWidth
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.stepWidth = stepWidth
        self.stepHeight = stepHeight
        self.argsStr = argsStr
        self.pixelThreshold = pixelThreshold
        self.drawBox = drawBox