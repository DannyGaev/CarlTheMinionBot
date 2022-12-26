
class Conversation:
  def __init__(self, userId, channelId):
    self.userId = userId
    self.channelId = channelId
  
  def getUserId(self):
    return self.userId

  def getChannelId(self):
    return self.channelId
    