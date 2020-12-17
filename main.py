from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json
from passkeys import letters, symbols, numbers

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#ffffff"
DARK_GREY = "#222831"
BLUE = "#31326f"


# ---------------------------- SEARCH USER DETAILS ------------------------------- #
def search():
    website_name = website_link_entry.get()
    try:
        with open("user_data.json", mode="r") as user_file:
            user_details = json.load(user_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="File Not Found ! \nNo data created")
    else:
        if website_name in user_details:
            user_email = user_details[website_name]["username"]
            user_password = user_details[website_name]["password"]
            messagebox.showinfo(title=website_name, message=f"Username: {user_email} \n"
                                                            f"Password: {user_password}")
        else:
            messagebox.showinfo(title="Not Found", message=f"No saved logins found for {website_name} exists")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    """ Creates a good secure password """
    pass_letters = [(choice(letters)) for _ in range(0, randint(8, 10))]
    pass_numbers = [choice(numbers) for _ in range(0, randint(2, 4))]
    pass_symbols = [choice(symbols) for _ in range(0, randint(3, 5))]

    password_list = pass_letters + pass_numbers + pass_symbols
    shuffle(password_list)

    # join iterables to string using join()
    PASSWORD = "".join(password_list)
    password_entry.insert(END, PASSWORD)
    pyperclip.copy(PASSWORD)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_details():
    """ Save user data to user db file """

    website = website_link_entry.get()
    username = email_or_username_entry.get()
    password = password_entry.get()
    new_userdata_dict = {website: {
        "username": username,
        "password": password
    }}
    if len(password) < 8 or len(website) == 0:
        messagebox.showwarning(title="Password Validation",
                               message="Empty Fields are not allowed ! "
                                       "Please fill up accurate data"
                                       "password need to be of at least 8 characters "
                               )
    else:
        input_res = messagebox.askokcancel(title="Verification", message=f"Confirm Your Details !")
        if input_res:
            try:
                with open("user_data.json", mode="r") as data_file:
                    # Step 1: fetch all the data from the file
                    user_data = json.load(data_file)
            except FileNotFoundError:
                # Step 2 : create a file
                with open("user_data.json", mode="w") as data_file:
                    json.dump(new_userdata_dict, data_file, indent=4)
            else:
                # Step 3 : update the file as per requirement
                user_data.update(new_userdata_dict)
                # Step 4: add data to the file in either of Step2 or Step3
                with open("user_data.json", mode="w") as data_file:
                    json.dump(user_data, data_file, indent=4)
            finally:
                website_link_entry.delete(0, len(website))
                password_entry.delete(0, len(password))


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=WHITE)

# password manager canvas
canvas = Canvas(width=200, height=200, bg="#fff", highlightthickness=0)
pm_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pm_image)
canvas.grid(column=1, row=0)
# entry inputs
website_link_entry = Entry(width=35)
website_link_entry.grid(column=1, row=1)
website_link_entry.focus()
email_or_username_entry = Entry(width=35)
email_or_username_entry.grid(column=1, row=2)
email_or_username_entry.insert(END, "user@email.com")
password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)
# entry labels
website_label = Label(text="Website: ", bg=WHITE)
website_label.grid(column=0, row=1)
email_or_username_label = Label(text="Email/Username: ", bg=WHITE)
email_or_username_label.grid(column=0, row=2)
password_label = Label(text="Password: ", bg=WHITE)
password_label.grid(column=0, row=3)
# buttons
search_user_details_btn = Button(text="Search", bg=DARK_GREY, fg=WHITE, width=15, command=search)
search_user_details_btn.grid(column=2, row=1)
generate_password_btn = Button(text="Generate Password", bg=WHITE, command=generate_password)
generate_password_btn.grid(column=2, row=3)
add_btn = Button(text="Add", bg=BLUE, fg=WHITE, width=45, command=save_details)
add_btn.grid(column=1, row=4, columnspan=2)
# continue window until exit
window.mainloop()
