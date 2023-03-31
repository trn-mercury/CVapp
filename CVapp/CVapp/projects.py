class Project:
    def __init__(self, id, title, role, start_date, end_date, description, bullets):
        self.id = id
        self.title = title
        self.role = role
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.bullets = bullets

    def getBullets(self):
        return self.bullets

class Bullet:
    def __init__(self, id, text):
        self.id = id
        self.text = text