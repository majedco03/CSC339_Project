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
        # onother dictionary to hold the lambda moves as:
        #  numOfStep : {
        #               fromStates: set of current states before processing the lambda move
        #               toStates: set of states after processing the lambda move
        #               isAccepted: boolean indicating if the NFA is in an accepting state after processing
        #              }
        
        self.results = []
        self.lambdaresults = []
    
    # this function will record a move
    def recordMove(self, symbol: str, fromStates: set[int], toStates: set[int], isAccepted: bool, numOfStep):
        self.results.append({
            numOfStep: {
                        "symbol": symbol,
                        "fromStates": fromStates,
                        "toStates": toStates, 
                        "isAccepted": isAccepted,
            }
        })
    # this function will record a lambda move
    def recordLambdaMove(self, fromStates: set[int], toStates: set[int], isAccepted: bool, numOfStep):
            self.lambdaresults.append({
                numOfStep: {
                            "fromStates": fromStates,
                            "toStates": toStates, 
                            "isAccepted": isAccepted,
                }
            })

    # this function will return the recorded results as a list of dictionaries
    def getResults(self):
        results_combined = []
        lambda_index = 0
        for step_index in range(len(self.results)):
            # Add lambda moves that occurred before this step
            while (lambda_index < len(self.lambdaresults) and
                   list(self.lambdaresults[lambda_index].keys())[0] <= step_index):
                results_combined.append(self.lambdaresults[lambda_index])
                lambda_index += 1
            # Add the actual move
            results_combined.append(self.results[step_index])
        # Add any remaining lambda moves
        while lambda_index < len(self.lambdaresults):
            results_combined.append(self.lambdaresults[lambda_index])
            lambda_index += 1
        return results_combined