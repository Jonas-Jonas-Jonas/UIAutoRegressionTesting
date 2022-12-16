from PIL import Image
import pytesseract # Libary for OCR
import re # Libary for Regex
import mss.tools # Libary used for taking screenshots of the monitor
import pyautogui
import time 
from skimage.metrics import structural_similarity
import cv2
import os
import sys
import numpy as np

def GodkjentOCR():
    with mss.mss() as sct:
        # Taking region screenshot of terminal window.
        monitor = {"top": 365, "left": 140, "width": 165, "height": 137}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    # Converting the img file to a string and storing it in the variable.
    image_text = pytesseract.image_to_string(Image.open('sct-365x140_165x137.png'))
    
    # ---------------------------------------------------------------------------

    # Regex filtering for "Godkjent" message in ProTouch Terminal Window.
    regex = r"\bGodkjent+"

    matches = re.search(regex, image_text)


    if matches:
        print ("Payment godkjent")
        accepted = True
         
    else:
        print("Waiting for payment")
        accepted = False
        
    return accepted

    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# OpenCV matching test on adding 2 products to the basket.
def SSIM_Basket_Test():
    
    with mss.mss() as sct:
        # Taking region screenshot of the basked window.
        monitor = {"top": 125, "left": 1512, "width": 408, "height": 950}
        output = r"C:\QA-Automated-Testing\model\TablesTerminalNormal\Actual\Actual-2-Products-In-Basket.jpeg".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    
    time.sleep(0.2)
    # Structural Similarity Index (SSIM)
    first = cv2.imread(r'C:\QA-Automated-Testing\model\TablesTerminalNormal\Actual\Actual-2-Products-In-Basket.jpeg')
    second = cv2.imread(r'C:\QA-Automated-Testing\model\TablesTerminalNormal\Expected\ExpectedBasket.jpeg')

    # Convert images to grayscale
    first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    score, diff = structural_similarity(first_gray, second_gray, full=True)
    print("Similarity Score: {:.3f}%".format(score * 100))

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type so we must convert the array 
    # to 8-bit unsigned integers in the range [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions that differ between the two images
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Highlight differences
    mask = np.zeros(first.shape, dtype='uint8')
    filled = second.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 100:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(first, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(second, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (0,255,0), -1)
            cv2.drawContours(filled, [c], 0, (0,255,0), -1)

    if score > 0.99:
        print("Test Sucess: Added 2 products to basket.")
    else:
        print("TEST FAILURE: PRODUCTS MISSING IN BASKET!")
        cv2.imshow('Actual Result', first)
        cv2.imshow('Expected Result', second)
        cv2.waitKey(0)
        sys.exit()

# --------------------------------------------------------------------------

# Verifies Table 313 still exists when going back to the table window to restore it.
def SSIM_Table_Still_Exist_After_Placement():
    
    with mss.mss() as sct:
        # Taking region screenshot of the basked window.
        monitor = {"top": 243, "left": 993, "width": 65, "height": 45}
        output = r"C:\QA-Automated-Testing\model\TablesTerminalNormal\Actual\Actual_Restore_Order_From_Table.jpeg".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    time.sleep(0.2)
    # Structural Similarity Index (SSIM)
    first = cv2.imread(r'C:\QA-Automated-Testing\model\TablesTerminalNormal\Actual\Actual_Restore_Order_From_Table.jpeg')
    second = cv2.imread(r'C:\QA-Automated-Testing\model\TablesTerminalNormal\Expected\Expected_Restore_Order_From_Table.jpeg')

    # Convert images to grayscale
    first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    score, diff = structural_similarity(first_gray, second_gray, full=True)
    print("Similarity Score: {:.3f}%".format(score * 100))

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type so we must convert the array 
    # to 8-bit unsigned integers in the range [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions that differ between the two images
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Highlight differences
    mask = np.zeros(first.shape, dtype='uint8')
    filled = second.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 100:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(first, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(second, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (0,255,0), -1)
            cv2.drawContours(filled, [c], 0, (0,255,0), -1)

    if score > 0.99:
        print("Test Sucess: Restored order from Table 313")
    else:
        print("TEST FAILURE: Table is empty")
        cv2.imshow('Actual Result', first)
        cv2.imshow('Expected Result', second)
        cv2.waitKey(0)
        sys.exit()

# ---------------------------------------------------------


# Verifies the order have been restored from the table with the correct amout and products. And if the table has not been multiplied or any changes to the table.
def SSIM_Restore_From_Table_Check():
    
    with mss.mss() as sct:
        # Taking region screenshot of the basked window.
        monitor = {"top": 125, "left": 1512, "width": 408, "height": 950}
        output = r"C:\QA-Automated-Testing\model\TablesTerminalNormal\Actual\Actual-Restore-Table-Check.jpeg".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    
    time.sleep(0.2)
    # Structural Similarity Index (SSIM)
    first = cv2.imread(r'C:\QA-Automated-Testing\model\TablesTerminalNormal\Actual\Actual-Restore-Table-Check.jpeg')
    second = cv2.imread(r'C:\QA-Automated-Testing\model\TablesTerminalNormal\Expected\Expected-Restore-Table-Check.jpeg')

    # Convert images to grayscale
    first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    score, diff = structural_similarity(first_gray, second_gray, full=True)
    print("Similarity Score: {:.3f}%".format(score * 100))

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type so we must convert the array 
    # to 8-bit unsigned integers in the range [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions that differ between the two images
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Highlight differences
    mask = np.zeros(first.shape, dtype='uint8')
    filled = second.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 100:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(first, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(second, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (0,255,0), -1)
            cv2.drawContours(filled, [c], 0, (0,255,0), -1)

    if score > 0.99:
        print("Test Sucess: Table have the same products as before.")
    else:
        print("TEST FAILURE: Table has been modified. duplicate products or missing products.")
        cv2.imshow('Actual Result', first)
        cv2.imshow('Expected Result', second)
        cv2.waitKey(0)
        sys.exit()
        




# --------------------------------------------------------------------------

def SSIM_Return_To_Shopping_Cart_After_Sucessfull_Payment():
    
    with mss.mss() as sct:
        # Taking region screenshot of the basked window.
        monitor = {"top": 60, "left": 0, "width": 1920, "height": 1020}
        output = r"C:\QA-Automated-Testing\model\TablesTerminalNormal\Actual\Actual_Payment_Succesfull.jpeg".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    time.sleep(0.2)
    # Structural Similarity Index (SSIM)
    first = cv2.imread(r'C:\QA-Automated-Testing\model\TablesTerminalNormal\Actual\Actual_Payment_Succesfull.jpeg')
    second = cv2.imread(r'C:\QA-Automated-Testing\model\TablesTerminalNormal\Expected\Expected_Payment_Succesfull.jpeg')

    # Convert images to grayscale
    first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    score, diff = structural_similarity(first_gray, second_gray, full=True)
    print("Similarity Score: {:.3f}%".format(score * 100))

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type so we must convert the array 
    # to 8-bit unsigned integers in the range [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions that differ between the two images
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Highlight differences
    mask = np.zeros(first.shape, dtype='uint8')
    filled = second.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 100:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(first, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(second, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (0,255,0), -1)
            cv2.drawContours(filled, [c], 0, (0,255,0), -1)

    if score > 0.99:
        print("Test Sucess: Returned to main shopping cart after payment is sucessfull.")
    else:
        print("TEST FAILURE: Could not return to main shopping cart.")
        cv2.imshow('Actual Result', first)
        cv2.imshow('Expected Result', second)
        os.system('taskkill /f /im PTClient.exe')
        cv2.waitKey(0)
        sys.exit()



# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Normal payment with tables.
def tablesnormal():
    for i in range(1, 10):

        # Select PT window
        pyautogui.moveTo(122, 32, duration = 0.5)
        pyautogui.click()

        # Select product tile "Hovedretter"
        pyautogui.moveTo(389, 862, duration = 1)
        pyautogui.click()


        # Select 2 products, "Krydret Fiskeburger med chilimajones" and "Kotelletter i form"
        pyautogui.moveTo(1338, 260, duration = 1)
        pyautogui.click()
        pyautogui.moveTo(671, 244, duration = 1)
        pyautogui.click()

        time.sleep(0.5)
        SSIM_Basket_Test() # OpenCV - SSIM
        

        # Place on table
        pyautogui.moveTo(1719, 1022, duration = 1)
        pyautogui.click()

        # Select Rom 4
        pyautogui.moveTo(875, 829, duration = 1)
        pyautogui.click()

        #  Select Table 313
        pyautogui.moveTo(1018, 274, duration = 1)
        pyautogui.click()

        # Select table
        pyautogui.moveTo(1719, 1022, duration = 1)
        pyautogui.click()

        time.sleep(0.5)
        SSIM_Table_Still_Exist_After_Placement()
        #  Select Table 313 to retrive order
        pyautogui.moveTo(1018, 274, duration = 1)
        pyautogui.click()

        time.sleep(0.5)
        SSIM_Restore_From_Table_Check()
        #  Go to payment window
        pyautogui.moveTo(1841, 1031, duration = 1)
        pyautogui.click()


        # Pay with Terminal (Integrert)
        pyautogui.moveTo(970, 178, duration = 1)
        pyautogui.click()


        # Verifying there is a "Godkjent" transaction from terminal window using neural network for Optical character recognition.
        timeout = time.time() + 30 # 30 seconds from now
        while True:
            test = 0
            accepted = GodkjentOCR()
            time.sleep(0.2)
            if accepted:
                break
            # Logic for aborting loop if terminal window times out.
            if test == 1 or time.time() > timeout:
                break
            test = test - 1

        time.sleep(1)
        SSIM_Return_To_Shopping_Cart_After_Sucessfull_Payment()


