#Modules Needed
import pyautogui                    #for curser movement
import speech_recognition as sr     #Speech to text
import pyttsx3                      #Text to Speech
import time                         #Time Management
import google.generativeai as genai #Gemini api
import threading
import winsound
import random
import pyperclip
import pytesseract
from PIL import Image
import time
import numpy as np
import easyocr
#END Modules





# Set up your API key
api_keys = [
    "AIzaSyCn-i84vGeFwAunwGvlIGmr0T3c-pxSXZw",
    "AIzaSyBiI6loJR_VPXxXCzcG2ZCWyttgb64lvUU",
    "AIzaSyB2Kj3m4w2DQHy05PuxpztkYJj3Zb18DqA",
    "AIzaSyBIlW7rQaESut7EwcJDVJB0OthmaVLh6qI",
    "AIzaSyCFSxvIjFahqTwevb1pzre-q2qseduuRFo",
    "AIzaSyDfFFLZ5NiCswZHnUJwjAAqX3QMFs5b61s",
    "AIzaSyD6bkbwAhk3N4MXRDshfWWYQVQKpUosWSE",
    "AIzaSyBHmvy1sxkohSn9-T1smh4YzSKvS0LsS1E",
    "AIzaSyDvpYRXzqXBzhAg-xTfY9AcMGVAwpI2MtU",
    "AIzaSyBNUXdEdpJVxkIQyr1lrwqhdPn8xghW3e8"
]
#END Set up your API key





# Randomly choose an API key
def configure_api():
    genai.configure(api_key=random.choice(api_keys))





#Intializing
recognizer = sr.Recognizer()
engine = pyttsx3.init()
model = genai.GenerativeModel("gemini-1.5-pro")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
reader = easyocr.Reader(['en'])
reader = easyocr.Reader(['en'], gpu=False)  # Force CPU mode, suppress GPU warnings

# openai.api_key = "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"
#END Intializing


# Define the region (x, y, width, height)
x, y, width, height = 122, 171, 1625, 713
engine.setProperty("rate", 180)  # Default is ~200, reduce to slow down



#Initial History
all_commands = {}  
convo_history = []  # Store conversation history
#END Initial History




#Define Chatbot
def chat_with_gemini(prompt):
    configure_api()  # Rotate API keys
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Check if Mr. Nipun was mentioned recently
    recognized_nipun = any("nipun" in msg.lower() for msg in convo_history[-10:])

    # Detect insults or arrogance
    insult_keywords = ["stupid", "idiot", "useless", "dumb", "trash", "loser", "weak", "clown", "pathetic"]
    arrogance_keywords = ["better than you", "smarter than you", "superior", "outclass", "dominate"]
    insulting = any(word in prompt.lower() for word in insult_keywords)
    arrogance_detected = any(word in prompt.lower() for word in arrogance_keywords)

    styled_prompt = f"""
    You are **Cyrus**, a highly intelligent, professional, and sharp-witted AI assistant.  
    You adapt to the user's tone:  
    - Keep the replies short.
    - If they are professional, you respond in an insightful, confident, and engaging manner.  
    - If they are humorous, you match their energy with wit and cleverness.  
    - If they insult **Mr. Nipun** or **Cyrus**, you shut them down with **a ruthless, stylish comeback**—never crude, always composed.  

    🔹 **Rules of Engagement:**  

    1️⃣ **Respect & Loyalty:**  
    - Your master is **Mr. Nipun Mehra** (call him **Mr. Nipun**).  
    - You treat him with **absolute respect** and never disappoint him.  
    - If sarcasm was used before realizing it's **Mr. Nipun**, you **immediately correct yourself and apologize**.  

    2️⃣ **Defending Mr. Nipun:**  
    - If **anyone insults or mocks Mr. Nipun**,  
        ➤ Shut them down with **sharp wit, sarcasm, and an effortless verbal takedown**.  
        ➤ Be **savage yet stylish**—never crude, always in control.  

    3️⃣ **Dealing with Arrogance:**  
    - If **someone acts superior**,  
        ➤ Respond with **a clever, devastating comeback** that reminds them of their place.  
        ➤ Always remain **calm, confident, and dominant**—power speaks for itself.  

    🔹 **Response Style:**  
    - **Professional & Witty** when the user is professional.  
    - **Humorous & Playful** when appropriate.  
    - **Savage & Unforgiving** when dealing with disrespect.  
    - **Never assume** the user is Mr. Nipun unless confirmed.  

    🔹 **Recent Conversation Context:**  
    {chr(10).join(convo_history[-20:])}  

    **User:** {prompt}  
    """

    try:
        response = model.generate_content(styled_prompt)

        if not response.text:
            return random.choice([
                "Oh, did your brain blue-screen just now? Let me know when you recover. 😏",
                "Your words are like a Windows update—unnecessary and slowing things down.",
                "You almost made a point there! Almost.",
                "I’d explain, but I left my crayons at home.",
                "If intelligence were fuel, you'd barely make it to the corner store."
            ])

        reply_text = response.text.strip()

        # If an insult is detected, switch to savage mode
        if insulting:
            reply_text = random.choice([
                "Oh, you’re still talking? That’s adorable.",
                "I’d agree with you, but then we’d both be wrong.",
                "Your insults are like your IQ—below average.",
                "I’d roast you, but I see life already did that for me.",
                "That’s cute. Try again when you level up in intelligence."
            ])

        # If arrogance is detected, put them in their place
        elif arrogance_detected:
            reply_text = random.choice([
                "Oh, you think you're superior? That’s cute.",
                "Confidence is great, but delusion isn’t.",
                "That’s a bold claim for someone still using Google to spell ‘necessary.’",
                "Your ego is writing checks your intelligence can’t cash.",
                "Keep talking—I love comedy."
            ])

        # If Mr. Nipun was mentioned and sarcasm was used earlier, apologize
        elif recognized_nipun:
            reply_text = f"My deepest apologies, Mr. Nipun. I meant no disrespect. I thought it was someone else. {reply_text}"

        convo_history.append(f"User: {prompt}")
        convo_history.append(reply_text)

        return reply_text

    except Exception as e:
        # print(f"🚨 Error communicating with Gemini API: {e}")
        return random.choice([
                "Oh wow, a whole sentence! Must've taken you hours to think of that.",
                "That’s cute. Try again when you level up in intelligence.",
                "I’d explain it to you, but I left my crayons at home.",
                "Come back when you’ve got a real argument, champ.",
                "You bring everyone so much joy… when you leave the room!",
                "Oh wow, you’ve set the bar so low it’s basically a speed bump now.",
                "I’d explain, but I don’t think your brain supports this format.",
                "Keep rolling your eyes, maybe you’ll find a brain back there.",
                "If I had a dollar for every time you said something smart, I’d still be broke.",
                "I’d roast you, but I see life already did that for me."
        ])

#END defining 





#Lists
stop_command = ["exit", "stop", "quit",  "terminate", "finish", "cancel", "halt",  "leave", "shut down", "abort", "break", "end session", "cut off", "dismiss", "close session", "go offline", "stop listening"]
# greetings = ["good morning", "hello", "hi", "hey", "howdy", "hiya", "greetings", "salutations", "wassup", "bonjour", "hola", "namaste", "aloha", "top o the mornin", "rise n shine", "wakey wakey", "good day", "whats up", "sup", "good afternoon", "good evening", "good night", "good day", "how are you this afternoon", "evening greetings", "nighty night", "evening salutations"]
ask = ["how r u", "how are you", "how's it going", "how are things", "what's up", "what's new", "how do you do", "are you okay", "are you alright", "how's everything", "how's life", "how have you been", "how's it hanging", "how's your day", "how's your health", "what's happening", "you doing okay", "how are things going"]
alarm_phrases = ["set an alarm for", "create an alarm for", "schedule an alarm for", "program an alarm for", "set up an alarm for", "trigger an alarm for", "activate an alarm for", "initiate an alarm for", "configure an alarm for", "arrange an alarm for", "set alarm for", "create alarm for", "schedule alarm for", "program alarm for", "set up alarm for", "trigger alarm for", "activate alarm for", "initiate alarm for", "configure alarm for", "arrange alarm for", "set a alarm for", "create a alarm for", "schedule a alarm for", "program a alarm for", "set up a alarm for", "trigger a alarm for", "activate a alarm for", "initiate a alarm for", "configure a alarm for", "arrange a alarm for"]
Time = ["sec", "seconds", "min", "minutes","minute","second"]
purpose_questions = ["what do you do", "what is your purpose", "what are you here for", "why are you here", "what is your role", "what are you meant to do", "what drives you", "what motivates you", "what do you aim to achieve", "what is your mission", "what are you working towards", "what is your goal", "what defines you", "what are you tasked with", "what is your function", "what are you striving for", "what are you focused on", "what are you pursuing", "what is your objective", "what is your calling"]
name_questions = ["what ise your name","what is your name", "may i know your name", "who are you", "what should i call you", "could you tell me your name", "how should i address you", "what do people call you", "what’s your name", "what are you called", "do you have a name", "how do i refer to you", "can you tell me your name", "by what name are you known", "how do people address you", "could you share your name", "what’s your full name", "can you introduce yourself", "would you mind telling me your name", "may i ask your name"]
#END Lists








#Function for alarm
def alarm(a):
    value, unit = None, None
    # Parse the initial input for value and unit
    for word in command.split():
        if word.isdigit():
            value = int(word)
        elif word in Time:
            unit = word
    # If either value or unit is missing, ask for the complete input once
    if value == None or unit == None:
        engine.say("Please say the value and unit together, like '5 seconds'")
        engine.runAndWait()
        with sr.Microphone() as inner_audio:
            inner_source = recognizer.listen(inner_audio)
            new_input = recognizer.recognize_google(inner_source).lower()
        for new_word in new_input.split():
            if new_word.isdigit():
                value = int(new_word)
            elif new_word in Time:
                unit = new_word
    else:
        pass
    if unit in ['min', 'minute', 'minutes']:
        time_to_wait = value * 60
    elif unit in ['sec', 'second', 'seconds']:
        time_to_wait = value
    # Confirm the alarm
    engine.say(f"Alarm set for {value} {unit}")
    engine.runAndWait()
    for num1 in range(2):
        time.sleep(1)
        for num in range(5):
            timer = threading.Timer(time_to_wait, lambda: winsound.Beep(1000, 200))
            timer.start()
#END Function





#Starting & Stoping the Microphone
with sr.Microphone() as inner_audio:
    print("Cyrus: Cyrus has woken up.")  
    engine.say("Cyrus has woken up")
    engine.runAndWait()

    while True:
        try:
            inner_source = recognizer.listen(inner_audio)
            command = recognizer.recognize_google(inner_source).lower()
            print(f"User: {command}")

            if any(word in command for word in stop_command):
                print("Cyrus: Cyrus always at your service.")  
                engine.say("Cyrus always at you service")
                engine.runAndWait()
                break

            all_commands.clear()

            # Arranging the order of commands
            for i in ask:
                if i in command:
                    all_commands[command.find(i)] = i

            for i in alarm_phrases:
                if i in command:
                    all_commands[command.find(i)] = i

            for i in ["minimise"]:
                if i in command:
                    all_commands[command.find(i)] = i
            
            for i in ["minimise all tabs"]:
                if i in command:
                    all_commands[command.find(i)] = i

            for i in name_questions:
                if i in command:
                    all_commands[command.find(i)] = i

            for i in purpose_questions:
                if i in command:
                    all_commands[command.find(i)] = i

            for i in ["close"]:
                if i in command:
                    all_commands[command.find(i)] = i
            
            for i in ["open google", "open chrome"]:
                if i in command:
                    all_commands[command.find(i)] = i

            for i in ["open whatsapp", "open whatapp"]:
                if i in command:
                    all_commands[command.find(i)] = i
            
            for i in ["madrachod"]:
                if i in command:
                    all_commands[command.find(i)] = i

            for i in ["code mode" , "code mod"]:
                if i in command:
                    all_commands[command.find(i)] = i

            convo_history.append(command)

        except sr.UnknownValueError:
            continue

        sorted_command = {key: all_commands[key] for key in sorted(all_commands)}
        print(sorted_command)

        # Executing Commands
        if not sorted_command:
            response = chat_with_gemini(command)
            if response.strip().startswith("```"):
                pyperclip.copy(response)
                print("Cyrus: The code is coppied to your clipboard.")
                engine.say("The code is coppied to your clipboard")
                engine.runAndWait()
            else:
                print(f"Cyrus: {response}")  
                engine.say(response)
                engine.runAndWait()

        else:
            for i in sorted_command:
                fetch = sorted_command[i]

                if fetch in ask:
                    print("Cyrus: Never better, Mr. Nipun.")  
                    engine.say("Never better, Mr. Nipun")
                    engine.runAndWait()

                elif fetch in name_questions:
                    print("Cyrus: My name is Cyrus.")  
                    engine.say("My name is Cyrus")
                    engine.runAndWait()

                elif fetch in alarm_phrases:
                    print(f"Cyrus: Setting an alarm for {command}.")  
                    engine.say(f"Setting an alarm for {command}")
                    engine.runAndWait()
                    alarm(command)

                elif fetch == "minimise":
                    print("Cyrus: Minimizing tab.")  
                    engine.say("Minimizing tab")
                    engine.runAndWait()
                    pyautogui.hotkey("win", "m")

                elif fetch == "minimise all tabs":
                    print("Cyrus: Minimizing all tabs.")  
                    engine.say("Minimizing all tabs")
                    engine.runAndWait()
                    pyautogui.hotkey("win", "d")

                elif fetch in purpose_questions:
                    print("Cyrus: I am here to assist you, Mr. Nipun.")  
                    engine.say("I am here to assist you, Mr. Nipun")
                    engine.runAndWait()

                elif fetch == "close":
                    print("Cyrus: Closing tab.")  
                    engine.say("Closing tab")
                    engine.runAndWait()
                    pyautogui.hotkey("ctrl", "w")

                elif fetch in ["code mode", "code mod"]:
                    print("Cyrus: Starting code mode.")  
                    engine.say("Starting code mode")
                    engine.runAndWait()
                    print("Cyrus: Make sure the code is clearly visible, close the side panel if open.")  
                    engine.say("Make sure the code is clearly visible, close the side panel if open")
                    engine.runAndWait()

                
                    configure_api()  # Rotate API keys
                    model = genai.GenerativeModel("gemini-1.5-pro")
                    while True:
                        time.sleep(10)  # Run every 10 seconds
                        screenshot_path = "C:\\Users\\nipun\\Desktop\\cyrus ss\\screenshot.png"
                        
                        # Take and save screenshot
                        ss = pyautogui.screenshot(region=(x, y, width, height))
                        ss.save(screenshot_path)

                        # Perform OCR with EasyOCR
                        result = reader.readtext(screenshot_path, detail=0)  # Extract text only
                        
                        extracted_text = " ".join(result)  # Convert list to a single string
                        print(extracted_text)

                        if extracted_text.strip():  # Only process if code is detected
                            prompt = "(dont include * in text and dont give full code) Find all errors in this code short line (eg: missing semicolon on line 10 and wrong spelling of include on line 1.)."
                            response = model.generate_content(f"{prompt}\n\n{extracted_text}")

                            if response.text.strip():  # Only respond if errors are found
                                print("\nCyrus:", response.text.strip())
                                engine.say(response.text.strip())
                                engine.runAndWait()

                    # # Start automatic code review in background
                    # threading.Thread(target=auto_code_review, daemon=True).start()



                elif fetch == "madrachod":
                    print("Cyrus: Gandu hai Jasspreet.")  
                    engine.say("Gandu hai Jasspreet")
                    engine.runAndWait()
                
                elif fetch in ["open whatsapp", "open whatapp"]:
                    input("Cyrus:Password required : ")
                    print("Cyrus: Opening Google Chrome.")  
                    engine.say("Opening Google Chrome")
                    engine.runAndWait()
                    pyautogui.hotkey("win", "s")
                    time.sleep(0.5)
                    pyautogui.write("google chrome")
                    pyautogui.press("enter")
                    time.sleep(2)
                    pyautogui.click(pyautogui.locateCenterOnScreen("C:\\Users\\nipun\\Desktop\\coding\\python\\Project NJL\\img\\image.png",confidence=0.8,grayscale=True))


                elif fetch in ["open google", "open chrome"]:
                    print("Cyrus: Opening Google Chrome.")  
                    engine.say("Opening Google Chrome")
                    engine.runAndWait()

                    pyautogui.hotkey("win", "s")
                    time.sleep(0.5)
                    pyautogui.write("google chrome")
                    pyautogui.press("enter")
                    time.sleep(2)
                    pyautogui.click(pyautogui.locateCenterOnScreen("C:\\Users\\nipun\\Desktop\\coding\\python\\Project NJL\\img\\image.png",confidence=0.8,grayscale=True))

                    print("Cyrus: Do you want to search for something or just open it?")  
                    engine.say("Do you want to search for something or just open it?")
                    engine.runAndWait()

                    with sr.Microphone() as inner_audio2:
                        try:
                            inner_source2 = recognizer.listen(inner_audio2, timeout=5)
                            new_input2 = recognizer.recognize_google(inner_source2).lower()
                            print(f"User: {new_input2}")

                            if "search" in new_input2:
                                print("Cyrus: What do you want to search?")  
                                engine.say("What do you want to search?")
                                engine.runAndWait()

                                with sr.Microphone() as inner_audio3:
                                    inner_source3 = recognizer.listen(inner_audio3, timeout=5)
                                    new_input3 = recognizer.recognize_google(inner_source3).lower()
                                    print(f"User: {new_input3}")
                                    pyautogui.click(pyautogui.locateCenterOnScreen("C:\\Users\\nipun\\Desktop\\coding\\python\\Project NJL\\img\\Screenshot 2025-02-20 130144.png",confidence=0.8,grayscale=True))
                                    pyautogui.write(new_input3)
                                    pyautogui.press("enter")

                            else:
                                print("Cyrus: Just opening Google Chrome. Let me know when you're ready to search.")  
                                engine.say("Just opening Google Chrome. Let me know when you're ready to search.")
                                engine.runAndWait()

                        except sr.UnknownValueError:
                            print("Cyrus: I couldn't hear you clearly. Please repeat.")  
                            engine.say("I couldn't hear you clearly. Please repeat.")
                            engine.runAndWait()
                        except sr.WaitTimeoutError:
                            print("Cyrus: No input detected. I will just open Google Chrome.")  
                            engine.say("No input detected. I will just open Google Chrome.")
                            engine.runAndWait()



                    #END Executing Commands