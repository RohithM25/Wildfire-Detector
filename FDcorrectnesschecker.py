#will return 0 if image processed incorrectly, 1 if image was processed incorrectly, and -1 if the correctness is unknown
def checkCorrectness(image, detected):
    if image == "sf6-resized1000,500.jpeg": return 1 if detected else 0
    elif image == "sf6.2.jpg": return 1 if detected else 0
    elif image == "sf6.3.jpg": return 1 if detected else 0
    elif image == "sf6.5.jpg": return 1 if detected else 0
    elif image == "sf6-no fire.jpg": return 1 if not detected else 0
    elif image == "sf6-no smoke.jpg": return 1 if detected else 0
    elif image == "sf6-no water.jpg": return 1 if detected else 0
    elif image == "sf6-very small fire.jpg": return 1 if detected else 0
    elif image == "hazmonDB1.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB2.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB3.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB4.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB5.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB6.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB7.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB8.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB9.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB10.jpeg": return 1 if not detected else 0
    elif image == "hazmonDB11.jpeg": return 1 if not detected else 0
    else: return -1