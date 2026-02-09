user=input("You:").lower()
bot=""   #response variable
if user=="hi":
   bot="hello"
elif user=="hello":
     bot="how may i assist you"
elif user=="name":
     bot="i am simple chatbot"
elif user=="bye":
     bot="good bye have a great day"
else:
     bot="i dont understand"
print("Bot:",bot)     