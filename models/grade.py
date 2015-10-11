# -*- coding: utf-8 -*-
class Grade:
    'A class that is a reference to an individual grade that a student recieves along with the assignment details.'

    def __init__(self, id,gName, dispDate, dAssigned, duDate, gArea, totalScore, scored):
        self.ID = id
        self.name = gName
        self.displayDate = dispDate
        self.dateAssigned = dAssigned
        self.dueDate = duDate
        self.gradingArea = gArea
        self.score = totalScore
        self.isScored = scored

    
    #getters
    def getID(self):
        return self.ID
    def getName(self):
        return self.name
    def getDisplayDate(self):
        return self.displayDate
    def getDateAssigned(self):
        return self.dateAssigned
    def getDueDate(self):
        return self.dueDate
    def getGradingArea(self):
        return self.gradingArea
    def getScore(self):
        return self.score
    def getIsScored(self):
        return self.isScored
    
    #setters
    def setID(self, id):
        self.ID = id
    def setName(self,name):
        self.name = name
    def setDisplayDate(self,dispDate):
        self.displayDate = dispDate
    def setDateAssigned(self,dAssigned):
        self.DateAssigned = dAssigned
    def setDueDate(self,pWord):
        self.password = pWord
    def setGradingArea(self,gArea):
        self.gradingArea = gArea
    def setScore(self,totalScore):
        self.score = totalScore
    def setIsScored(self,scored):
        self.isScored = scored
