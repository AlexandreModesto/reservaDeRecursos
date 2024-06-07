class Resource():
    def __init__(self,type, approver, email, requester, reason, date, hour, status):
        self.type=type
        self.approver = approver
        self.email = email
        self.requester = requester
        self.reason = reason
        self.date = date
        self.hour = hour
        self.status = status
