import datetime
lines = "--------------------------------------------"

def welcome():
  return "Hello! I'm Carl. What can I help you with?\n-Type 'complaint' to submit a complaint\n-Type 'suggestion' to submit a suggestion\n-For other types of messages, feel free to send the whole thing here, though the first two types will generally get priority!\n\n(Any sort of message will be recieved anonymously!)"

def complaintToBOT_OWNER(issue):
  return "{divide}\n".format(divide=lines)+r"**Carl Complaint Recieved:**"+"\n-On date & time: {dateTime}\n-Complaint was: '{complaint}'".format(dateTime=datetime.datetime.now().strftime("%c"),complaint=issue)+"\n{divide}".format(divide=lines)

def suggestionToBOT_OWNER(suggestion):
  return "{divide}\n".format(divide=lines)+r"**Carl Suggestion Recieved:**"+"\n-On date & time: {dateTime}\n-Suggestion was: '{suggest}'".format(dateTime=datetime.datetime.now().strftime("%c"),suggest=suggestion)+"\n{divide}".format(divide=lines)

def generalMessageToBOT_OWNER(generalMessage):
  return "{divide}\n".format(divide=lines)+r"**Carl General Message Recieved:**"+"\n-On date & time: {dateTime}\n-Message was: '{message}'".format(dateTime=datetime.datetime.now().strftime("%c"),message=generalMessage)+"\n{divide}".format(divide=lines)

