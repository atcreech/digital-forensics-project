import tkinter as tk
from tkinter import scrolledtext as st
import sqlite3 as sql
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np

# Base Window
root = tk.Tk()
root.title("Image Analyzer")
root.geometry('1200x700')

# Label prompting the user to enter a path
lbl = tk.Label(root, text="Select Mounting Location: ", font=("Arial", 24))
lbl.place(relx=0.50, rely=0.4, anchor="center")

# Text box allowing user to enter path to image location
txt = tk.Entry(root, width=50)
txt.place(relx=0.50, rely=0.5, anchor="center")

# Investigator's information
name = ""
case_num = ""
case_name = ""
dept_name = ""

# Will be used to determine where files are located
path = ""
desktop_path = ""


# Window to enter credentials into
def name_window():

    # Setting up the window
    window = tk.Toplevel(root)
    window.title("Enter Credentials")
    window.geometry('400x600')

    name_lbl = tk.Label(window, text="Name of Investigator:")
    name_lbl.place(relx=0.1, rely=0.1)

    # Space for user to enter name
    name_box = tk.Entry(window, width=15)
    name_box.place(relx=0.5, rely=0.1)

    case_num_lbl = tk.Label(window, text="Case Number:")
    case_num_lbl.place(relx=0.1, rely=0.2)

    # Space for user to enter case number
    case_num_box = tk.Entry(window, width=15)
    case_num_box.place(relx=0.5, rely=0.2)

    case_name_lbl = tk.Label(window, text="Case Name:")
    case_name_lbl.place(relx=0.1, rely=0.3)

    # Space for user to enter case name
    case_name_box = tk.Entry(window, width=15)
    case_name_box.place(relx=0.5, rely=0.3)

    dept_name_lbl = tk.Label(window, text="Department Name:")
    dept_name_lbl.place(relx=0.1, rely=0.4)

    # Space for user to enter department name
    dept_name_box = tk.Entry(window, width=15)
    dept_name_box.place(relx=0.5, rely=0.4)

    # Button that when pressed will save credentials and open a new window with info_window()
    cred_btn = tk.Button(window, text="Save Credentials", fg="black", command=lambda: cred_click(name_box,
                                                                                                 case_num_box,
                                                                                                 case_name_box,
                                                                                                 dept_name_box,
                                                                                                 window))
    cred_btn.place(relx=0.3, rely=0.6)


# Method that saves credentials, closes the credential window, and initiates the information window
def cred_click(name_box, case_num_box, case_name_box, dept_name_box, window):

    global name, case_num, case_name, dept_name

    name = name_box.get()
    case_num = case_num_box.get()
    case_name = case_name_box.get()
    dept_name = dept_name_box.get()
    window.destroy()
    info_window()


# Method used for creating bar graphs
def graph_input(x_list, y_list, title):

    # Step size is determined based on maximum y-value to ensure readability
    step_size = 1

    if max(y_list) >= 20:

        step_size = 5

    if max(y_list) >= 100:

        step_size = 10

    if max(y_list) >= 200:

        step_size = 50

    if max(y_list) >= 1000:

        step_size = 100

    fig, ax = plt.subplots()

    # Creation of bar graph
    ax.bar(x_list, y_list, width=1, edgecolor="white", linewidth=0.7)
    ax.set(xlim=(-0.5, len(x_list) - 0.5), xticks=np.arange(0, len(x_list)), ylim=(0, max(y_list) + 3 * step_size),
           yticks=np.arange(0, max(max(y_list) + 3 * step_size, 11), step=step_size))
    plt.title(title)
    plt.show()


# Method used to create pie chart for usage statistics
def plot_usage(x_list, y_list):

    plt.pie(y_list, labels=x_list)
    plt.title("Usage Statistics")
    plt.show()


# Method for outputting analysis information to a file
def to_file(profile, browser_list, useful_chrome_urls, useful_chrome_downloads, useful_chrome_searches,
            useful_chrome_logins, useful_chrome_autofill, useful_edge_urls, useful_edge_downloads,
            useful_edge_searches, useful_edge_autofill, useful_edge_logins, useful_firefox_urls,
            useful_firefox_downloads, useful_firefox_searches, useful_firefox_bookmarks, useful_firefox_cookies,
            desktop_list, download_list, document_list, picture_list, video_list, onedrive_list, recent_list,
            recycle_list, app_local_list, app_locallow_list, app_roaming_list, program_list, program86_list):

    global desktop_path, name, case_name, case_num, dept_name

    # Opens a new file for writing or overwrites a currently existing file
    fp = open(desktop_path[:-5] + "/" + profile + "_analysis.txt", 'w')

    # Information is written into file
    fp.write("Output of Forensic Analysis of Windows Disk Image\n\n")
    fp.write("Forensic Examiner: " + name + "\n")
    fp.write("Case Name: " + case_name + "\n")
    fp.write("Case Number: " + case_num + "\n")
    fp.write("Department Name: " + dept_name + "\n\n")
    fp.write("Profile: " + profile + "\n\n")
    fp.write("Installed Browsers: " + browser_list + "\n\n")
    fp.write("Chrome History\n\n" + useful_chrome_urls + "\n\n")
    fp.write("Chrome Downloads\n\n" + useful_chrome_downloads + "\n\n")
    fp.write("Chrome Searches\n\n" + useful_chrome_searches + "\n\n")
    fp.write("Chrome Logins\n\n" + useful_chrome_logins + "\n\n")
    fp.write("Chrome Autofill\n\n" + useful_chrome_autofill + "\n\n")
    fp.write("Edge History\n\n" + useful_edge_urls + "\n\n")
    fp.write("Edge Downloads\n\n" + useful_edge_downloads + "\n\n")
    fp.write("Edge Searches\n\n" + useful_edge_searches + "\n\n")
    fp.write("Edge Autofill\n\n" + useful_edge_autofill + "\n\n")
    fp.write("Edge Logins\n\n" + useful_edge_logins + "\n\n")
    fp.write("Firefox History\n\n" + useful_firefox_urls + "\n\n")
    fp.write("Firefox Downloads\n\n" + useful_firefox_downloads + "\n\n")
    fp.write("Firefox Searches\n\n" + useful_firefox_searches + "\n\n")
    fp.write("Firefox Bookmarks\n\n" + useful_firefox_bookmarks + "\n\n")
    fp.write("Firefox Cookies\n\n" + useful_firefox_cookies + "\n\n")
    fp.write("\nWindows Artifacts\n\n")
    fp.write("Desktop Files\n\n" + desktop_list + "\n\n")
    fp.write("Download Files\n\n" + download_list + "\n\n")
    fp.write("Document Files\n\n" + document_list + "\n\n")
    fp.write("Picture Files\n\n" + picture_list + "\n\n")
    fp.write("Video Files\n\n" + video_list + "\n\n")
    fp.write("OneDrive Files\n\n" + onedrive_list + "\n\n")
    fp.write("Recent Items\n\n" + recent_list + "\n\n")
    fp.write("Recycle Bin\n\n" + recycle_list + "\n\n")
    fp.write("AppData/Local\n\n" + app_local_list + "\n\n")
    fp.write("AppData/LocalLow\n\n" + app_locallow_list + "\n\n")
    fp.write("AppData/Roaming\n\n" + app_roaming_list + "\n\n")
    fp.write("Program Files\n\n" + program_list + "\n\n")
    fp.write("Program Files(x86)\n\n" + program86_list + "\n\n")

    # File is closed to disallow further alteration
    fp.close()


# Information window for disk image
def info_window():

    global path, desktop_path

    # Setting up window
    window = tk.Toplevel(root)
    window.title("Information")
    window.geometry('1368x768')
    window_canvas = tk.Canvas(window)
    vbar = tk.Scrollbar(window, orient="vertical", command=window_canvas.yview)  # Used to scroll through the info
    vbar.pack(side="right", fill="y")
    window_canvas.configure(yscrollcommand=vbar.set)
    frame = tk.Frame(window_canvas, width=1368, height=10000)
    window_canvas.pack(side="left", fill="both", expand=True)
    window_canvas.create_window(0, 0, window=frame, anchor="nw")
    title_size = 36
    heading_size = 24
    text_size = 16
    label_spacing = 75
    text_spacing = 375

    profile_names_list = ""
    useful_profiles = []

    # Finds all profiles listed on the machine
    for profile in os.listdir(path + "/Users"):

        if '.' not in profile:

            profile_names_list += profile + ", "

        if '.' not in profile and "Public" not in profile and "Default" not in profile and "User" not in profile:

            useful_profiles.append(profile)

    if len(profile_names_list) > 2:

        profile_names_list = profile_names_list[:-2]

    # Displays all profiles to the user
    profile_names_lbl = tk.Label(frame, text="Profiles: " + profile_names_list, font=("Arial", text_size))
    profile_names_lbl.place(relx=0.05, y=50)

    y_offset = 150  # Variable used for vertical placement of widgets in frame

    # Iterates through every profile
    for profile in useful_profiles:

        # Lists active profile for analysis
        profile_lbl = tk.Label(frame, text="Active Profile: " + profile, font=("Arial", title_size))
        profile_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += 100

        installed_browsers = []  # Browsers installed on the machine
        normal_browsers = []    # Browsers installed on the machine excluding Firefox

        # Path to browser data
        browser_path = path + "/Users/" + profile + "/AppData/Local"

        # Path to firefox data
        firefox_profile_path = path + "/Users/" + profile + "/AppData/Roaming/Mozilla/Firefox/Profiles"

        # Finds specific profile used in Firefox
        for folder in os.listdir(firefox_profile_path):

            if "release" in folder:

                firefox_profile_path += "/" + folder
                break

        # Arrays used for statistics
        browser_url_count = []
        browser_download_count = []
        browser_search_count = []
        browser_autofill_count = []
        browser_login_count = []

        # Formatted strings containing Chrome information
        chrome_url_list = ""
        chrome_download_list = ""
        chrome_search_list = ""
        chrome_autofill_list = ""
        chrome_logins_list = ""

        # Integers to keep track of number of items
        chrome_url_count = 0
        chrome_download_count = 0
        chrome_search_count = 0
        chrome_autofill_count = 0
        chrome_login_count = 0

        # Formatted strings containing Edge information
        edge_url_list = ""
        edge_download_list = ""
        edge_search_list = ""
        edge_autofill_list = ""
        edge_logins_list = ""

        # Integers to keep track of number of items
        edge_url_count = 0
        edge_download_count = 0
        edge_search_count = 0
        edge_autofill_count = 0
        edge_login_count = 0

        # Formatted strings containing Firefox information
        firefox_url_list = ""
        firefox_download_list = ""
        firefox_cookie_list = ""
        firefox_search_list = ""
        firefox_bookmark_list = ""

        # Integers to keep track of number of items
        firefox_url_count = 0
        firefox_download_count = 0
        firefox_cookie_count = 0
        firefox_search_count = 0
        firefox_bookmark_count = 0

        # Iterates through to determine if browsers are installed
        for file in os.listdir(browser_path):

            # If Google has software installed
            if "Google" in file:

                # Iterates through folders and files in "Google" directory
                for directory in os.listdir(browser_path + "/Google"):

                    # If Chrome is installed
                    if "Chrome" in directory:

                        # Updates information
                        installed_browsers.append("Chrome")
                        normal_browsers.append("Chrome")
                        browser_url_count.append(0)
                        browser_download_count.append(0)
                        browser_search_count.append(0)
                        browser_autofill_count.append(0)
                        browser_login_count.append(0)

                        # Connects to the sql file containing Chrome history information
                        history = sql.connect(browser_path + "/Google/Chrome/User Data/Default/History")
                        history_cursor = history.cursor()

                        # Selects information specific to urls, stored in tuple
                        history_cursor.execute('SELECT url, title FROM urls')
                        history_url_output = history_cursor.fetchall()

                        # Iterates through urls
                        for row in history_url_output:

                            count = 0   # Used to keep track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                chrome_url_list += element + "\n\n\n"

                                if count != 0:

                                    # Separator
                                    chrome_url_list += "------------------------------------------------------------" \
                                                       "------------------------------------------------------------" \
                                                       "------------------------------\n"

                                count = 1

                            # More formatting and updating values/lists
                            chrome_url_list += "\n\n"
                            chrome_url_count += 1
                            browser_url_count[len(installed_browsers) - 1] += 1

                        # Selects download information in tuple format
                        history_cursor.execute('SELECT target_path, tab_url FROM downloads')
                        history_downloads = history_cursor.fetchall()

                        # Iterates through each tuple
                        for row in history_downloads:

                            count = 0   # Used to keep track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                chrome_download_list += element + "\n\n\n"

                                if count != 0:

                                    # Separator
                                    chrome_download_list += "-------------------------------------------------------" \
                                                            "-------------------------------------------------------" \
                                                            "----------------------------------------\n\n"

                                count = 1

                            # More formatting and updating values/lists
                            chrome_download_list += "\n\n"
                            chrome_download_count += 1
                            browser_download_count[len(installed_browsers) - 1] += 1

                        # Selects search terms in tuple format
                        history_cursor.execute('SELECT term FROM keyword_search_terms')
                        history_terms = history_cursor.fetchall()

                        # Iterates through tuples
                        for row in history_terms:

                            # Iterates through elements in tuples
                            for element in row:

                                # Adds element to respective list
                                chrome_search_list += element + "\n\n"

                            # Updating values
                            chrome_search_count += 1
                            browser_search_count[len(installed_browsers) - 1] += 1

                        # Closes SQLite connection to file
                        history.close()

                        # Connects to file containing autofill information for Chrome
                        autofill = sql.connect(browser_path + "/Google/Chrome/User Data/Default/Web Data")
                        autofill_cursor = autofill.cursor()

                        # Selects autofill information in tuple format
                        autofill_cursor.execute('SELECT name, value FROM autofill')
                        autofill_terms = autofill_cursor.fetchall()

                        # Iterates through tuples
                        for row in autofill_terms:

                            count = 0   # Keeps track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                chrome_autofill_list += element + "\n\n\n"

                                if count != 0:

                                    # Separator
                                    chrome_autofill_list += "-------------------------------------------------------" \
                                                            "-------------------------------------------------------" \
                                                            "----------------------------------------\n"

                                count = 1

                            # More formatting and updating values/lists
                            chrome_autofill_list += "\n\n"
                            chrome_autofill_count += 1
                            browser_autofill_count[len(normal_browsers) - 1] += 1

                        # Closes SQLite connection to file
                        autofill.close()

                        # Connects to file containing login data for Google Chrome
                        logins = sql.connect(browser_path + "/Google/Chrome/User Data/Default/Login Data")
                        login_cursor = logins.cursor()

                        # Selects url and username info in tuple format
                        login_cursor.execute('SELECT origin_url, username_element, username_value FROM logins')
                        login_terms = login_cursor.fetchall()

                        # Iterates through tuples
                        for row in login_terms:

                            count = 0   # Used to keep track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                chrome_logins_list += element + "\n\n\n"

                                if count == 2:

                                    # Separator
                                    chrome_logins_list += "---------------------------------------------------------" \
                                                          "---------------------------------------------------------" \
                                                          "------------------------------------\n"

                                count += 1

                            # More formatting and updating values/lists
                            chrome_logins_list += "\n\n"
                            chrome_login_count += 1
                            browser_login_count[len(normal_browsers) - 1] += 1

                        # Closing SQLite connection to file
                        logins.close()

            # If Mozilla has software installed
            if "Mozilla" in file:

                # Iterates through every folder/file in "Mozilla" directory
                for directory in os.listdir(browser_path + "/Mozilla"):

                    # If Firefox is installed
                    if "Firefox" in directory:

                        # Updating values
                        installed_browsers.append("Firefox")
                        browser_url_count.append(0)
                        browser_download_count.append(0)
                        browser_search_count.append(0)

                        # Used to determine path of this python file
                        full_path = os.path.realpath(__file__)
                        file_path = os.path.dirname(full_path)

                        # Sets value temporarily
                        desktop_path = file_path

                        # If this file is on the desktop or in a subdirectory of the desktop
                        if "Desktop" in file_path:

                            has_temp = False    # Does not have a Temp folder

                            # If Temp folder exists
                            if "Temp" in os.listdir(file_path):

                                desktop_path = file_path + "/Temp"  # Sets path to Temp folder
                                has_temp = True

                            # If Temp folder doesn't exist
                            if not has_temp:

                                # Creates Temp folder and sets path to Temp folder
                                os.mkdir(file_path + "/Temp")
                                desktop_path = file_path + "/Temp"

                        # If desktop is not in path to this file
                        else:

                            index = 0
                            count = 0

                            # Truncates the file path to just the first two elements, i.e. "/home/alex"
                            for i in range(len(file_path)):

                                if "/" in str(file_path[i]):

                                    count += 1

                                if count == 2:

                                    index = i + 1

                            # Temporary path to desktop
                            temp_path = file_path[:index] + "/Desktop"

                            has_temp = False

                            # Creates Temp folder if not present and sets path to Temp folder
                            for desktop_folder in os.listdir(temp_path):

                                if "Temp" in desktop_folder:

                                    desktop_path = temp_path + "/Temp"
                                    has_temp = True

                            if not has_temp:

                                os.mkdir(temp_path + "/Temp")
                                desktop_path = temp_path + "/Temp"

                        # Copies necessary information to Temp folder
                        shutil.copy(firefox_profile_path + "/places.sqlite", desktop_path)
                        shutil.copy(firefox_profile_path + "/formhistory.sqlite", desktop_path)
                        shutil.copy(firefox_profile_path + "/cookies.sqlite", desktop_path)

                        # Connects to file containing Firefox information
                        places = sql.connect(desktop_path + "/places.sqlite")
                        place_cursor = places.cursor()

                        # Selects url information in tuple format
                        place_cursor.execute('SELECT url, title FROM moz_places')
                        place_terms = place_cursor.fetchall()

                        # Iterates through tuples
                        for row in place_terms:

                            count = 0   # Keeps track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                firefox_url_list += str(element) + "\n\n\n"

                                if count == 1:

                                    # Separator
                                    firefox_url_list += "-----------------------------------------------------------" \
                                                        "-----------------------------------------------------------" \
                                                        "--------------------------------\n"

                                count = 1

                            # More formatting and updating values/lists
                            firefox_url_list += "\n\n"
                            firefox_url_count += 1
                            browser_url_count[len(installed_browsers) - 1] += 1

                        # Selects download information in tuple format
                        place_cursor.execute('SELECT content FROM moz_annos')
                        download_terms = place_cursor.fetchall()

                        # Iterates through tuples
                        for row in download_terms:

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds elements to respective list
                                firefox_download_list += str(element) + "\n\n"

                            # Updating values
                            firefox_download_count += 1
                            browser_download_count[len(installed_browsers) - 1] += 1

                        # Selects bookmark data in tuple format
                        place_cursor.execute('SELECT title FROM moz_bookmarks')
                        bookmark_terms = place_cursor.fetchall()

                        # Iterates through tuples
                        for row in bookmark_terms:

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                firefox_bookmark_list += str(element) + "\n\n"

                            # Updates value
                            firefox_bookmark_count += 1

                        # Closes SQLite connection to file
                        places.close()

                        # Connects to file with search history of Firefox
                        form_history = sql.connect(desktop_path + "/formhistory.sqlite")
                        form_cursor = form_history.cursor()

                        # Selects search information in tuple format
                        form_cursor.execute('SELECT value FROM moz_formhistory')
                        form_terms = form_cursor.fetchall()

                        # Iterates through tuples
                        for row in form_terms:

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                firefox_search_list += str(element) + "\n\n"

                            # Updating values
                            firefox_search_count += 1
                            browser_search_count[len(installed_browsers) - 1] += 1

                        # Closes SQLite connection to file
                        form_history.close()

                        # Connects to file containing cookie data for Firefox
                        cookie_file = sql.connect(desktop_path + "/cookies.sqlite")
                        cookie_cursor = cookie_file.cursor()

                        # Selects cookie information in tuple format
                        cookie_cursor.execute('SELECT name, value, host FROM moz_cookies')
                        cookie_terms = cookie_cursor.fetchall()

                        # Iterates through tuples
                        for row in cookie_terms:

                            count = 0   # Keeps track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                firefox_cookie_list += str(element) + "\n\n\n"

                                if count == 2:

                                    # Separator
                                    firefox_cookie_list += "--------------------------------------------------------" \
                                                           "--------------------------------------------------------" \
                                                           "--------------------------------------\n"

                                count += 1

                            # More formatting and updating values
                            firefox_cookie_list += "\n\n"
                            firefox_cookie_count += 1

                        # Closes SQLite connection to file
                        cookie_file.close()

            # If Microsoft has software installed
            if "Microsoft" in file:

                # Iterates through files/folders in Microsoft directory
                for directory in os.listdir(browser_path + "/Microsoft"):

                    # If Microsoft Edge is installed
                    if "Edge" in directory:

                        # Updates necessary information
                        installed_browsers.append("Microsoft Edge")
                        normal_browsers.append("Microsoft Edge")
                        browser_url_count.append(0)
                        browser_download_count.append(0)
                        browser_search_count.append(0)
                        browser_autofill_count.append(0)
                        browser_login_count.append(0)

                        # Connects to file containing history information for Edge
                        history = sql.connect(browser_path + "/Microsoft/Edge/User Data/Default/History")
                        history_cursor = history.cursor()

                        # Selects url information in tuple format
                        history_cursor.execute("SELECT url, title FROM urls")
                        url_terms = history_cursor.fetchall()

                        # Iterates through tuples
                        for row in url_terms:

                            count = 0   # Keeps track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                edge_url_list += element + "\n\n\n"

                                if count == 1:

                                    # Separator
                                    edge_url_list += "--------------------------------------------------------------" \
                                                     "--------------------------------------------------------------" \
                                                     "--------------------------\n"

                                count = 1

                            # More formatting and updating values/lists
                            edge_url_list += "\n\n"
                            edge_url_count += 1
                            browser_url_count[len(installed_browsers) - 1] += 1

                        # Selects download information in tuple format
                        history_cursor.execute('SELECT target_path, tab_url FROM downloads')
                        download_terms = history_cursor.fetchall()

                        # Iterates through tuples
                        for row in download_terms:

                            count = 0   # Keeps track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                edge_download_list += element + "\n\n\n"

                                if count == 1:

                                    # Separator
                                    edge_download_list += "----------------------------------------------------------" \
                                                          "----------------------------------------------------------" \
                                                          "----------------------------------\n"

                                count = 1

                            # More formatting and updating values/lists
                            edge_download_list += "\n\n"
                            edge_download_count += 1
                            browser_download_count[len(installed_browsers) - 1] += 1

                        # Selects search information in tuple format
                        history_cursor.execute('SELECT term FROM keyword_search_terms')
                        search_terms = history_cursor.fetchall()

                        # Iterates through tuples
                        for row in search_terms:

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                edge_search_list += element + "\n\n"

                            # Updating values/lists
                            edge_search_count += 1
                            browser_search_count[len(installed_browsers) - 1] += 1

                        # Closes SQLite connection to file
                        history.close()

                        # Connects to file containing autofill information for Edge
                        autofill = sql.connect(browser_path + "/Microsoft/Edge/User Data/Default/Web Data")
                        autofill_cursor = autofill.cursor()

                        # Selects autofill information in tuple format
                        autofill_cursor.execute('SELECT name, value FROM autofill')
                        autofill_terms = autofill_cursor.fetchall()

                        # Iterates through tuples
                        for row in autofill_terms:

                            count = 0   # Keeps track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                edge_autofill_list += element + "\n\n\n"

                                if count == 1:

                                    # Separator
                                    edge_autofill_list += "---------------------------------------------------------" \
                                                          "---------------------------------------------------------" \
                                                          "------------------------------------\n"

                                count = 1

                            # More formatting and updating values/lists
                            edge_autofill_list += "\n\n"
                            edge_autofill_count += 1
                            browser_autofill_count[len(normal_browsers) - 1] += 1

                        # Closes SQLite connection to file
                        autofill.close()

                        # Connects to file containing login information for Edge
                        logins = sql.connect(browser_path + "/Microsoft/Edge/User Data/Default/Login Data")
                        login_cursor = logins.cursor()

                        # Selects url and username information in tuple format
                        login_cursor.execute('SELECT origin_url, username_element, username_value FROM logins')
                        login_terms = login_cursor.fetchall()

                        # Iterates through tuples
                        for row in login_terms:

                            count = 0   # Keeps track of position in tuple

                            # Iterates through elements in tuple
                            for element in row:

                                # Adds element to respective list
                                edge_logins_list += element + "\n\n\n"

                                if count == 2:

                                    # Separator
                                    edge_logins_list += "---------------------------------------------------------" \
                                                        "---------------------------------------------------------" \
                                                        "------------------------------------\n"

                                count += 1

                            # More formatting and updating values/lists
                            edge_logins_list += "\n\n"
                            edge_login_count += 1
                            browser_login_count[len(normal_browsers) - 1] += 1

                        # Closes SQLite connection to file
                        logins.close()

        browser_list = ""

        # Adds installed browsers to list
        for browser in installed_browsers:

            browser_list += browser + ", "

        browser_list = browser_list[:-2]    # Formatting

        # Displays installed browsers to user
        browser_lbl = tk.Label(frame, text="Installed Browsers: " + browser_list, font=("Arial", text_size))
        browser_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        # If Chrome is installed
        if "Chrome" in browser_list:

            chrome_urls_lbl = tk.Label(frame, text="Chrome URL History", font=("Arial", heading_size))
            chrome_urls_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Chrome url information
            chrome_urls = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            chrome_urls.insert(tk.INSERT, chrome_url_list)
            chrome_urls.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of urls
            chrome_url_count_lbl = tk.Label(frame, text="Number of Items: " + str(chrome_url_count),
                                            font=("Arial", text_size))
            chrome_url_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            chrome_downloads_lbl = tk.Label(frame, text="Chrome Downloads History", font=("Arial", heading_size))
            chrome_downloads_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Chrome download information
            chrome_downloads = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            chrome_downloads.insert(tk.INSERT, chrome_download_list)
            chrome_downloads.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of downloads
            chrome_download_count_lbl = tk.Label(frame, text="Number of Items: " + str(chrome_download_count),
                                                 font=("Arial", text_size))
            chrome_download_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            chrome_search_lbl = tk.Label(frame, text="Chrome Searches", font=("Arial", heading_size))
            chrome_search_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Chrome search information
            chrome_searches = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            chrome_searches.insert(tk.INSERT, chrome_search_list)
            chrome_searches.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of searches
            chrome_search_count_lbl = tk.Label(frame, text="Number of Items: " + str(chrome_search_count),
                                               font=("Arial", text_size))
            chrome_search_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            chrome_autofill_lbl = tk.Label(frame, text="Chrome Autofill", font=("Arial", heading_size))
            chrome_autofill_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Chrome autofill information
            chrome_autofill = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            chrome_autofill.insert(tk.INSERT, chrome_autofill_list)
            chrome_autofill.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of autofill entries
            chrome_autofill_count_lbl = tk.Label(frame, text="Number of Items: " + str(chrome_autofill_count),
                                                 font=("Arial", text_size))
            chrome_autofill_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            chrome_login_lbl = tk.Label(frame, text="Chrome Logins", font=("Arial", heading_size))
            chrome_login_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Chrome login information
            chrome_logins = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            chrome_logins.insert(tk.INSERT, chrome_logins_list)
            chrome_logins.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of logins
            chrome_login_count_lbl = tk.Label(frame, text="Number of Items: " + str(chrome_login_count),
                                              font=("Arial", text_size))
            chrome_login_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

        # If Edge is installed
        if "Microsoft Edge" in browser_list:

            edge_url_lbl = tk.Label(frame, text="Edge History", font=("Arial", heading_size))
            edge_url_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Edge url information
            edge_urls = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            edge_urls.insert(tk.INSERT, edge_url_list)
            edge_urls.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of urls
            edge_url_count_lbl = tk.Label(frame, text="Number of Items: " + str(edge_url_count),
                                          font=("Arial", text_size))
            edge_url_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            edge_download_lbl = tk.Label(frame, text="Edge Downloads", font=("Arial", heading_size))
            edge_download_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Edge download information
            edge_downloads = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            edge_downloads.insert(tk.INSERT, edge_download_list)
            edge_downloads.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of downloads
            edge_download_count_lbl = tk.Label(frame, text="Number of Items: " + str(edge_download_count),
                                               font=("Arial", text_size))
            edge_download_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            edge_search_lbl = tk.Label(frame, text="Edge Searches", font=("Arial", heading_size))
            edge_search_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Edge search information
            edge_searches = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            edge_searches.insert(tk.INSERT, edge_search_list)
            edge_searches.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of searches
            edge_search_count_lbl = tk.Label(frame, text="Number of Items: " + str(edge_search_count),
                                             font=("Arial", text_size))
            edge_search_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            edge_autofill_lbl = tk.Label(frame, text="Edge Autofill", font=("Arial", heading_size))
            edge_autofill_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Edge autofill information
            edge_autofill = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            edge_autofill.insert(tk.INSERT, edge_autofill_list)
            edge_autofill.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of autofill entries
            edge_autofill_count_lbl = tk.Label(frame, text="Number of Items: " + str(edge_autofill_count),
                                               font=("Arial", text_size))
            edge_autofill_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            edge_login_lbl = tk.Label(frame, text="Edge Logins", font=("Arial", heading_size))
            edge_login_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Edge login information
            edge_logins = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            edge_logins.insert(tk.INSERT, edge_logins_list)
            edge_logins.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of Edge logins
            edge_login_count_lbl = tk.Label(frame, text="Number of Items: " + str(edge_login_count),
                                            font=("Arial", text_size))
            edge_login_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

        # If Firefox is installed
        if "Firefox" in browser_list:

            firefox_url_lbl = tk.Label(frame, text="Firefox History", font=("Arial", heading_size))
            firefox_url_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Firefox url information
            firefox_urls = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            firefox_urls.insert(tk.INSERT, firefox_url_list)
            firefox_urls.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of urls
            firefox_url_count_lbl = tk.Label(frame, text="Number of Items: " + str(firefox_url_count),
                                             font=("Arial", text_size))
            firefox_url_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            firefox_download_lbl = tk.Label(frame, text="Firefox Downloads", font=("Arial", heading_size))
            firefox_download_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Firefox download information
            firefox_downloads = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            firefox_downloads.insert(tk.INSERT, firefox_download_list)
            firefox_downloads.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of downloads
            firefox_download_count_lbl = tk.Label(frame, text="Number of Items: " + str(firefox_download_count),
                                                  font=("Arial", text_size))
            firefox_download_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            firefox_bookmark_lbl = tk.Label(frame, text="Firefox Bookmarks", font=("Arial", heading_size))
            firefox_bookmark_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Firefox bookmark information
            firefox_bookmarks = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            firefox_bookmarks.insert(tk.INSERT, firefox_bookmark_list)
            firefox_bookmarks.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of bookmarks
            firefox_bookmark_count_lbl = tk.Label(frame, text="Number of Items: " + str(firefox_bookmark_count),
                                                  font=("Arial", text_size))
            firefox_bookmark_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            firefox_search_lbl = tk.Label(frame, text="Firefox Searches", font=("Arial", heading_size))
            firefox_search_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Firefox search information
            firefox_searches = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            firefox_searches.insert(tk.INSERT, firefox_search_list)
            firefox_searches.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of searches
            firefox_search_count_lbl = tk.Label(frame, text="Number of Items: " + str(firefox_search_count),
                                                font=("Arial", text_size))
            firefox_search_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

            firefox_cookie_lbl = tk.Label(frame, text="Firefox Cookies", font=("Arial", heading_size))
            firefox_cookie_lbl.place(relx=0.50, y=y_offset, anchor="center")
            y_offset += label_spacing

            # Displays Firefox cookie information
            firefox_cookies = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
            firefox_cookies.insert(tk.INSERT, firefox_cookie_list)
            firefox_cookies.place(relx=0.05, y=y_offset)
            y_offset += text_spacing

            # Displays number of cookies
            firefox_cookie_count_lbl = tk.Label(frame, text="Number of Items: " + str(firefox_cookie_count),
                                                font=("Arial", text_size))
            firefox_cookie_count_lbl.place(relx=0.05, y=y_offset)
            y_offset += label_spacing

        local_artifacts_lbl = tk.Label(frame, text="OS Artifacts", font=("Arial", title_size))
        local_artifacts_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += 100

        documents_lbl = tk.Label(frame, text="Windows Documents", font=("Arial", heading_size))
        documents_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        documents_list = ""
        document_count = 0

        # Walks through Documents and finds all files in all subdirectories
        for root_path, directories, files in os.walk(path + "/Users/" + profile + "/Documents"):

            for file in files:

                if "desktop.ini" not in file:

                    documents_list += file + "\n\n"
                    document_count += 1

        # Displays document information
        documents = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        documents.insert(tk.INSERT, documents_list)
        documents.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of documents
        document_count_lbl = tk.Label(frame, text="Number of Items: " + str(document_count), font=("Arial", text_size))
        document_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        os_downloads_lbl = tk.Label(frame, text="Windows Downloads", font=("Arial", heading_size))
        os_downloads_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        os_downloads_list = ""
        os_download_count = 0

        # Walks through Downloads directory and finds all files in all subdirectories
        for root_path, directories, files in os.walk(path + "/Users/" + profile + "/Downloads"):

            for file in files:

                if "desktop.ini" not in file:

                    os_downloads_list += file + "\n\n"
                    os_download_count += 1

        # Displays download information
        os_downloads = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        os_downloads.insert(tk.INSERT, os_downloads_list)
        os_downloads.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of downloads
        os_download_count_lbl = tk.Label(frame, text="Number of Items: " + str(os_download_count),
                                         font=("Arial", text_size))
        os_download_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        onedrive_lbl = tk.Label(frame, text="Windows OneDrive", font=("Arial", heading_size))
        onedrive_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        onedrive_list = ""
        onedrive_count = 0

        # Walks through OneDrive directory and finds all files in all subdirectories
        for root_path, directories, files in os.walk(path + "/Users/" + profile + "/OneDrive"):

            for file in files:

                if "desktop.ini" not in file:

                    onedrive_list += file + "\n\n"
                    onedrive_count += 1

        # Displays onedrive information
        onedrive_text = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        onedrive_text.insert(tk.INSERT, onedrive_list)
        onedrive_text.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of onedrive elements
        onedrive_count_lbl = tk.Label(frame, text="Number of Items: " + str(onedrive_count), font=("Arial", text_size))
        onedrive_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        pictures_lbl = tk.Label(frame, text="Windows Pictures", font=("Arial", heading_size))
        pictures_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        pictures_list = ""
        picture_count = 0

        # Walks through Pictures directory and finds all files in all subdirectories
        for root_path, directories, files in os.walk(path + "/Users/" + profile + "/Pictures"):

            for file in files:

                if "desktop.ini" not in file:

                    pictures_list += file + "\n\n"
                    picture_count += 1

        # Displays picture information
        pictures = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        pictures.insert(tk.INSERT, pictures_list)
        pictures.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of pictures
        picture_count_lbl = tk.Label(frame, text="Number of Items: " + str(picture_count), font=("Arial", text_size))
        picture_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        video_lbl = tk.Label(frame, text="Windows Videos", font=("Arial", heading_size))
        video_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        video_list = ""
        video_count = 0

        # Walks through Videos directory and finds all files in all subdirectories
        for root_path, directories, files in os.walk(path + "/Users/" + profile + "/Videos"):

            for file in files:

                if "desktop.ini" not in file:

                    video_list += file + "\n\n"
                    video_count += 1

        # Displays video information
        videos = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        videos.insert(tk.INSERT, video_list)
        videos.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of video elements
        video_count_lbl = tk.Label(frame, text="Number of Items: " + str(video_count), font=("Arial", text_size))
        video_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        desktop_lbl = tk.Label(frame, text="Windows Desktop", font=("Arial", heading_size))
        desktop_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        desktop_list = ""
        desktop_count = 0

        # Walks through Desktop directory and finds all files in all subdirectories
        for root_path, directories, files in os.walk(path + "/Users/" + profile + "/Desktop"):

            for file in files:

                if "desktop.ini" not in file:

                    desktop_list += file + "\n\n"
                    desktop_count += 1

        # Displays desktop information
        desktop_text = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        desktop_text.insert(tk.INSERT, desktop_list)
        desktop_text.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of desktop elements
        desktop_count_lbl = tk.Label(frame, text="Number of Items: " + str(desktop_count), font=("Arial", text_size))
        desktop_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        recent_lbl = tk.Label(frame, text="Windows Recent Items", font=("Arial", heading_size))
        recent_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        recent_list = ""
        recent_count = 0

        # Walks through Recent directory and finds all files in all subdirectories
        for file in os.listdir(path + "/Users/" + profile + "/AppData/Roaming/Microsoft/Windows/Recent"):

            if "." in file and "desktop.ini" not in file:

                recent_list += file + "\n\n"
                recent_count += 1

        # Displays recent information
        recents = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        recents.insert(tk.INSERT, recent_list)
        recents.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of recent elements
        recent_count_lbl = tk.Label(frame, text="Number of Items: " + str(recent_count), font=("Arial", text_size))
        recent_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        recycle_lbl = tk.Label(frame, text="Windows Recycle Bin", font=("Arial", heading_size))
        recycle_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        recycle_list = ""
        recycle_count = 0

        # Walks through Recycle Bin and finds all files in all subdirectories
        for root_path, directories, files in os.walk(path + "/$Recycle.Bin"):

            for file in files:

                if "desktop.ini" not in file:

                    recycle_list += file + "\n\n"
                    recycle_count += 1

        # Displays all recycle bin information
        recycle_text = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        recycle_text.insert(tk.INSERT, recycle_list)
        recycle_text.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of recycle bin elements
        recycle_count_lbl = tk.Label(frame, text="Number of Items: " + str(recycle_count), font=("Arial", text_size))
        recycle_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        app_local_label = tk.Label(frame, text="Windows AppData/Local", font=("Arial", heading_size))
        app_local_label.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        app_local_list = ""
        app_local_count = 0

        # Walks through Local directory and finds all folders/files and subdirectories of folders
        for directory in os.listdir(path + "/Users/" + profile + "/AppData/Local"):

            # Is a file
            if "." in directory and "desktop.ini" not in directory:

                app_local_list += directory + "\n\n"
                app_local_list += "---------------------------------------------------------------------------------" \
                                  "---------------------------------------------------------------------\n\n"
                app_local_count += 1

            # Is a folder
            if "." not in directory and "desktop.ini" not in directory:

                app_local_list += directory + "\n\n"

                # Subdirectories
                for file in os.listdir(path + "/Users/" + profile + "/AppData/Local/" + directory):

                    if "desktop.ini" not in file:

                        app_local_list += "  --   " + file + "\n\n"
                        app_local_count += 1

                app_local_list += "---------------------------------------------------------------------------------" \
                                  "---------------------------------------------------------------------\n\n"

        # Displays Local information
        app_local_text = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        app_local_text.insert(tk.INSERT, app_local_list)
        app_local_text.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of Local elements
        app_local_count_lbl = tk.Label(frame, text="Number of Items (Subdirectories/Files): " + str(app_local_count),
                                       font=("Arial", text_size))
        app_local_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        app_locallow_lbl = tk.Label(frame, text="Windows AppData/LocalLow", font=("Arial", heading_size))
        app_locallow_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        app_locallow_list = ""
        app_locallow_count = 0

        # Walks through LocalLow directory and finds files/folders and subdirectories
        for directory in os.listdir(path + "/Users/" + profile + "/AppData/LocalLow"):

            # Is a file
            if "." in directory and "desktop.ini" not in directory:

                app_locallow_list += directory + "\n\n"
                app_locallow_list += "------------------------------------------------------------------------------" \
                                     "------------------------------------------------------------------------\n\n"
                app_locallow_count += 1

            # Isn't a file
            if "." not in directory and "desktop.ini" not in directory:

                app_locallow_list += directory + "\n\n"

                for file in os.listdir(path + "/Users/" + profile + "/AppData/LocalLow/" + directory):

                    if "desktop.ini" not in file:

                        app_locallow_list += "  --   " + file + "\n\n"
                        app_locallow_count += 1

                app_locallow_list += "------------------------------------------------------------------------------" \
                                     "------------------------------------------------------------------------\n\n"

        # Displays LocalLow information
        app_locallow_text = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        app_locallow_text.insert(tk.INSERT, app_locallow_list)
        app_locallow_text.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of LocalLow elements
        app_locallow_count_lbl = tk.Label(frame, text="Number of Items (Subdirectories/Files): " +
                                                      str(app_locallow_count), font=("Arial", text_size))
        app_locallow_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        app_roaming_lbl = tk.Label(frame, text="Windows AppData/Roaming", font=("Arial", heading_size))
        app_roaming_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        app_roaming_list = ""
        app_roaming_count = 0

        # Walks through Roaming directory and finds folders/files and subdirectories
        for directory in os.listdir(path + "/Users/" + profile + "/AppData/Roaming"):

            # Is a file
            if "." in directory and "desktop.ini" not in directory:

                app_roaming_list += directory + "\n\n"
                app_roaming_list += "-------------------------------------------------------------------------------" \
                                    "-----------------------------------------------------------------------\n\n"
                app_roaming_count += 1

            # Isn't a file
            if "." not in directory and "desktop.ini" not in directory:

                app_roaming_list += directory + "\n\n"

                for file in os.listdir(path + "/Users/" + profile + "/AppData/Roaming/" + directory):

                    if "desktop.ini" not in file:

                        app_roaming_list += "  --   " + file + "\n\n"
                        app_roaming_count += 1

                app_roaming_list += "-------------------------------------------------------------------------------" \
                                    "-----------------------------------------------------------------------\n\n"

        # Displays Roaming information
        app_roaming_text = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        app_roaming_text.insert(tk.INSERT, app_roaming_list)
        app_roaming_text.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of Roaming elements
        app_roaming_count_lbl = tk.Label(frame, text="Number of Items (Subdirectories/Files): " +
                                                     str(app_roaming_count), font=("Arial", text_size))
        app_roaming_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        program_lbl = tk.Label(frame, text="Windows Program Files", font=("Arial", heading_size))
        program_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        program_list = ""
        program_count = 0

        # Walks through Program Files directory and finds files/folders and subdirectories
        for directory in os.listdir(path + "/Program Files"):

            # Is a file
            if "." in directory and "desktop.ini" not in directory:

                program_list += directory + "\n\n"
                program_list += "-----------------------------------------------------------------------------------" \
                                "-------------------------------------------------------------------\n\n"
                program_count += 1

            # Isn't a file
            if "." not in directory and "desktop.ini" not in directory:

                program_list += directory + "\n\n"

                for file in os.listdir(path + "/Program Files/" + directory):

                    if "desktop.ini" not in file:

                        program_list += "  --   " + file + "\n\n"
                        program_count += 1

                program_list += "-----------------------------------------------------------------------------------" \
                                "-------------------------------------------------------------------\n\n"

        # Displays Program File information
        program_text = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        program_text.insert(tk.INSERT, program_list)
        program_text.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of Program File elements
        program_count_lbl = tk.Label(frame, text="Number of Items (Subdirectories/Files): " + str(program_count),
                                     font=("Arial", text_size))
        program_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        program86_lbl = tk.Label(frame, text="Windows Program Files(x86)", font=("Arial", heading_size))
        program86_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        program86_list = ""
        program86_count = 0

        # Walks through Program Files (x86) directory and finds files/folders and subdirectories
        for directory in os.listdir(path + "/Program Files (x86)"):

            # Is a file
            if "." in directory and "desktop.ini" not in directory:

                program86_list += directory + "\n\n"
                program86_list += "---------------------------------------------------------------------------------" \
                                  "---------------------------------------------------------------------\n\n"
                program86_count += 1

            # Isn't a file
            if "." not in directory and "desktop.ini" not in directory:

                program86_list += directory + "\n\n"

                for file in os.listdir(path + "/Program Files (x86)/" + directory):

                    if "desktop.ini" not in file:

                        program86_list += "  --   " + file + "\n\n"
                        program86_count += 1

                program86_list += "---------------------------------------------------------------------------------" \
                                  "---------------------------------------------------------------------\n\n"

        # Displays Program File (x86) Information
        program86_text = st.ScrolledText(frame, wrap=tk.WORD, width=150, height=20)
        program86_text.insert(tk.INSERT, program86_list)
        program86_text.place(relx=0.05, y=y_offset)
        y_offset += text_spacing

        # Displays number of Program File (x86) elements
        program86_count_lbl = tk.Label(frame, text="Number of Items (Subdirectories/Files): " + str(program86_count),
                                       font=("Arial", text_size))
        program86_count_lbl.place(relx=0.05, y=y_offset)
        y_offset += label_spacing

        browser_stats_lbl = tk.Label(frame, text="Browser Statistics", font=("Arial", title_size))
        browser_stats_lbl.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += label_spacing

        # Button for browser url statistics
        url_button = tk.Button(frame, text="Compare URL Stats", fg="black")
        url_button.place(relx=0.08, y=y_offset)

        if len(installed_browsers) > 1:

            url_button.configure(command=lambda: graph_input(installed_browsers, browser_url_count, "URL Statistics"))

        # Button for browser download statistics
        download_button = tk.Button(frame, text="Compare Download Stats", fg="black")
        download_button.place(relx=0.215, y=y_offset)

        if len(installed_browsers) > 1:

            download_button.configure(command=lambda: graph_input(installed_browsers, browser_download_count,
                                                                  "Download Statistics"))

        # Button for browser search statistics
        search_button = tk.Button(frame, text="Compare Search Stats", fg="black")
        search_button.place(relx=0.38, y=y_offset)

        if len(installed_browsers) > 1:

            search_button.configure(command=lambda: graph_input(installed_browsers, browser_search_count,
                                                                "Search Statistics"))

        # Button for browser autofill statistics
        autofill_button = tk.Button(frame, text="Compare Autofill Stats", fg="black")
        autofill_button.place(relx=0.53, y=y_offset)

        if len(normal_browsers) > 1:

            autofill_button.configure(command=lambda: graph_input(normal_browsers, browser_autofill_count,
                                                                  "Autofill Statistics"))

        # Button for browser login statistics
        login_button = tk.Button(frame, text="Compare Login Stats", fg="black")
        login_button.place(relx=0.68, y=y_offset)

        if len(normal_browsers) > 1:

            login_button.configure(command=lambda: graph_input(normal_browsers, browser_login_count,
                                                               "Login Statistics"))

        # Button for usage statistics
        usage_button = tk.Button(frame, text="Usage Stats", fg="black")
        usage_button.place(relx=0.83, y=y_offset)

        if len(installed_browsers) > 1:

            browser_usage_count = []

            # Adds information to get a picture of the total usage of each browser
            for i in range(0, len(installed_browsers)):

                browser_usage_count.append(browser_url_count[i] + browser_download_count[i] + browser_search_count[i])

            usage_button.configure(command=lambda: plot_usage(installed_browsers, browser_usage_count))

        y_offset += 100

        # Removes formatting
        useful_chrome_urls = chrome_url_list
        useful_chrome_urls = useful_chrome_urls.replace('-', '')

        # Removes formatting
        useful_chrome_downloads = chrome_download_list
        useful_chrome_downloads = useful_chrome_downloads.replace('-', '')

        # Removes formatting
        useful_chrome_searches = chrome_search_list
        useful_chrome_searches = useful_chrome_searches.replace('-', '')

        # Removes formatting
        useful_chrome_autofill = chrome_autofill_list
        useful_chrome_autofill = useful_chrome_autofill.replace('-', '')

        # Removes formatting
        useful_chrome_logins = chrome_logins_list
        useful_chrome_logins = useful_chrome_logins.replace('-', '')

        # Removes formatting
        useful_edge_urls = edge_url_list
        useful_edge_urls = useful_edge_urls.replace('-', '')

        # Removes formatting
        useful_edge_downloads = edge_download_list
        useful_edge_downloads = useful_edge_downloads.replace('-', '')

        # Removes formatting
        useful_edge_searches = edge_search_list
        useful_edge_searches = useful_edge_searches.replace('-', '')

        # Removes formatting
        useful_edge_autofill = edge_autofill_list
        useful_edge_autofill = useful_edge_autofill.replace('-', '')

        # Removes formatting
        useful_edge_logins = edge_logins_list
        useful_edge_logins = useful_edge_logins.replace('-', '')

        # Removes formatting
        useful_firefox_urls = firefox_url_list
        useful_firefox_urls = useful_firefox_urls.replace('-', '')

        # Removes formatting
        useful_firefox_downloads = firefox_download_list
        useful_firefox_downloads = useful_firefox_downloads.replace('-', '')

        # Removes formatting
        useful_firefox_searches = firefox_search_list
        useful_firefox_searches = useful_firefox_searches.replace('-', '')

        # Removes formatting
        useful_firefox_bookmarks = firefox_bookmark_list
        useful_firefox_bookmarks = useful_firefox_bookmarks.replace('-', '')

        # Removes formatting
        useful_firefox_cookies = firefox_cookie_list
        useful_firefox_cookies = useful_firefox_cookies.replace('-', '')

        # Removes formatting
        useful_local_list = app_local_list
        useful_local_list = useful_local_list.replace("  --   ", "  ..   ")
        useful_local_list = useful_local_list.replace('-', '')

        # Removes formatting
        useful_locallow_list = app_locallow_list
        useful_locallow_list = useful_locallow_list.replace("  --   ", "  ..   ")
        useful_locallow_list = useful_locallow_list.replace('-', '')

        # Removes formatting
        useful_roaming_list = app_roaming_list
        useful_roaming_list = useful_roaming_list.replace("  --   ", "  ..   ")
        useful_roaming_list = useful_roaming_list.replace('-', '')

        # Removes formatting
        useful_program_list = program_list
        useful_program_list = useful_program_list.replace("  --   ", "  ..   ")
        useful_program_list = useful_program_list.replace('-', '')

        # Removes formatting
        useful_program86_list = program86_list
        useful_program86_list = useful_program86_list.replace("  --   ", "  ..   ")
        useful_program86_list = useful_program86_list.replace('-', '')

        # Button to export information to file
        to_file_button = tk.Button(frame, text="Output to File", fg="black",
                                   command=lambda: to_file(profile, browser_list, useful_chrome_urls,
                                                           useful_chrome_downloads, useful_chrome_searches,
                                                           useful_chrome_logins, useful_chrome_autofill,
                                                           useful_edge_urls, useful_edge_downloads,
                                                           useful_edge_searches, useful_edge_autofill,
                                                           useful_edge_logins, useful_firefox_urls,
                                                           useful_firefox_downloads, useful_firefox_searches,
                                                           useful_firefox_bookmarks, useful_firefox_cookies,
                                                           desktop_list, os_downloads_list, documents_list,
                                                           pictures_list, video_list, onedrive_list, recent_list,
                                                           recycle_list, useful_local_list, useful_locallow_list,
                                                           useful_roaming_list, useful_program_list,
                                                           useful_program86_list))
        to_file_button.place(relx=0.50, y=y_offset, anchor="center")
        y_offset += 100

        # Configures scrollable area to allow all elements to be seen
        frame.configure(height=y_offset)

    # Updates scrollable area
    window.update()
    window_canvas.config(scrollregion=window_canvas.bbox("all"))


# Processes button press on first window
def button_click():

    global path

    # Sets path for image
    path = txt.get()

    # Detects if path is valid
    try:

        os.listdir(path)
        name_window()   # Opens credential window

    except FileNotFoundError:

        lbl.configure(text="Enter a Valid Path")


# Button to save image path and open credential window
btn = tk.Button(root, text="Open", fg="black", command=button_click, height=3, width=15)
btn.place(relx=0.50, rely=0.6, anchor="center")

# Starts first window
root.mainloop()
