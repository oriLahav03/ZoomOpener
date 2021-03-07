try:
    import sys
    from datetime import datetime
    import keyboard
    import pandas as pd
    import pyautogui
    import time
    from selenium import webdriver
except Exception as e:
    print(e)

print('Press Control C to exit any time you want!')

Weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

today = Weekdays[datetime.today().weekday()]
print("Today is", today)

with open(r'Files\registered.txt', 'r+') as register:
    ctx = register.readline()
    if ctx == 'False':
        register.truncate(0)
        print("Please change the following settings in the Zoom application for this program to work the best!")
        from PIL import Image

        instructions_img = Image.open(r"Files\buttons\Instructions.png")
        instructions_img.show()

        input('Press any key after you finish change the settings :)')
        file = open(r'Files\registered.txt', 'w')
        file.write('True')
        file.close()
    ctx = register.readline()

try:
    df = pd.read_csv(f'Files\\Days\\{today}.csv')
    df_new = pd.DataFrame()
except Exception as e:
    print(e)
    input()
    sys.exit()

print('Time now: ', datetime.now().strftime("%H:%M"))
print('Classes today at: ', df.Time.values)

try:
    while True:
        # Check the current system time
        time_str = datetime.now().strftime("%H:%M")
        # Check if the current time is mentioned in the Dataframe
        if time_str in df.Time.values:
            print("Joining class")

            df_new = df[df['Time'].astype(str).str.contains(time_str)]

            times = []
            for i in df.Time.values:
                times.append(i)

            links = []
            for i in df.Link.values:
                links.append(i)

            index = times.index(time_str)

            link_to_class = links[index]

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            try:
                dr = webdriver.Chrome(executable_path=r'Files\chromedriver.exe', options=chrome_options)
                dr.get(link_to_class)
            except Exception as e:
                print(e)

            time.sleep(10)

            position = pyautogui.locateOnScreen(r"Files\buttons\open_app_from_web.png", grayscale=True)
            if position is None:
                position = pyautogui.locateOnScreen(r"Files\buttons\open_app_from_web_light.png", grayscale=True)
            pyautogui.moveTo(position)
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            dr.close()
            time.sleep(2)

            passcodes = []
            for i in df.Passcode.values:
                passcodes.append(i)

            passcode = passcodes[index]

            position = pyautogui.locateOnScreen(r"Files\buttons\enter_pass.png", grayscale=True)

            if position is not None:
                if str(type(passcode)) == "<class 'numpy.float64'>":
                    new_pass = str(passcode)[:-2]
                else:
                    new_pass = str(passcode)

                keyboard.write(new_pass)
                position = pyautogui.locateOnScreen(r"Files\buttons\join_meeting.png", grayscale=True)
                pyautogui.moveTo(position)
                pyautogui.click()
            time.sleep(3)

            # Wait for one minute before the next iteration starts
            time.sleep(60)
except KeyboardInterrupt as e:
    pass
