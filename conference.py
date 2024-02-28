class ConferenceCall:
    def __init__(self, name, limit):
        self.name = name
        self.limit = limit
        self.members = []

    def add_member(self, member):
        if len(self.members) <= self.limit:
            self.members.append(member)
            print(f"{member} has joined the conference call.")
        else:
            print("Sorry, the conference call is full.")

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)
            print(f"{member} has left the conference call.")
        else:
            print(f"{member} is not currently in the conference call.")

    def list_members(self):
        print("Current members:")
        for member in self.memberstcp:
            print(member)