#this class will be just a DTO to hold the simulation data
class SimulationData:
    def __init__(self):
        # Dectionary to hold the simulation results as:
        #  numOfStep : {
        #               symbol : alphabet symbol
        #               fromStates: set of current states before processing the symbol
        #               toStates: set of states after processing the symbol
        #               isAccepted: boolean indicating if the NFA is in an accepting state after processing the symbol
        #              }
        self.results = []
    
    # this function will record a move
    def recordMove(self, symbol: str, fromStates: set[int], toStates: set[int], isAccepted: bool, numOfStep):
        self.results.append({
            numOfStep: {
                        "symbol": symbol,
                        "fromStates": fromStates,
                        "toStates": toStates, 
                        "isAccepted": isAccepted
            }
        })

    # this function will return the recorded results
    def getResults(self):
        return self.results