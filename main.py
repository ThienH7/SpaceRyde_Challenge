import numpy as np
import Plane, My_App, sys
from PyQt5 import QtWidgets

class Control():

    def _init__(self, runways, runway_dims):
        self.runways = [runways] # list of runways center
        self.runway_dims = [runway_dims]
        self.landing_queue = [] # size of number of runways
        self.holding_queue = []
        self.landing = []
        self.planes = {} # used to check updated set from node

        # Get the number of holding circles within a ring of radius i
        self.holding_circle_sizes = [int(np.pi / np.arcsin(1.0/i)) for i in range(1, 10)]
        self.holding_circle_max = [sum((self.holding_circle_sizes, [0, i + 1]) for i in range(len(self.holding_circle_sizes)))]

        for i in range(len(self.holding_circle_sizes)):
            self.holding_circle_max.append(sum(self.holding_circle_sizes))

    # Calculates the closest runway the trajectory change to land
    def landing_trajectory(self, plane):
        current_pos = plane[1]
        min_dist = float("inf")
        closest_runway = self.runways[0]
        trajectory = 0
        for runway in self.runways:
            x_dist = runway.x - current_pos[0]
            y_dist = runway.y - current_pos[1]
            dist = np.sqrt((x_dist)**2 + (y_dist)**2)
            
            if dist < min_dist:
                closest_runway = runway
                trajectory = np.arctan(y_dist / x_dist)
        
        return (closest_runway, trajectory)

    # Provides instructions for the node to give the plane to land
    def landing_sequence(self):
        for plane in self.landing_queue:
            if plane not in self.landing:
                new_heading = self.landing_trajectory(plane)
                # updateHeading(new_heading) # at node

    # Provides a new plane with a location to perform a holding pattern
    def holding(self, plane):
        currently_holding = len(self.landing_queue)
        for i in len(self.holding_circle_max):
            if currently_holding < self.holding_circle_max[i]:
                self.landing_queue.append(plane)
                if i == 0:
                    holdX = (i + 1.0 * np.cos(np.pi/currently_holding + 1))
                    holdY = (i + 1.0 * np.sin(np.pi/currently_holding + 1))
                else:
                    holdX = (i + 1.0 * np.cos(np.pi/currently_holding - self.holding_circle_max[i - 1] + 1))
                    holdY = (i + 1.0 * np.sin(np.pi/currently_holding - self.holding_circle_max[i - 1] + 1))
                return[holdX, holdY]

    # Once a plane has landed update the queue for next plan to land
    def update_queue(self):
        self.landing.append(self.landing_queue.pop())
        self.landing_sequence()

    def control_traffic(self):

        updated_queue = [aircraft]
        
        while(True):
            # updated_queue = ATC.request_planes() # Get new planes and position
            # landed = ATC.landed() # Get landed planes to remove

            while updated_queue:
                # next_plane = updated_queue.get()
                next_plane = updated_queue.pop()
                holding_pos = self.holding(next_plane)
                next_plane.updating_holding(holding_pos) # Send to node
                self.landing_queue.append(next_plane)
                updated_queue.remove(next_plane)
                

            # for plane in landed:
            #     self.landing.remove(plane)

            if len(self.landing) < len(self.runways):
                self.landing_sequence()

            
            
if __name__ == "__main__":
    control = Control()
    aircraft = Plane.Plane()
    app = QtWidgets.QApplication(sys.argv)
    window = My_App.My_App([0,0])
    
    window.show()

    sys.exit(app.exec_())

    while(True):
        aircraft.update_pos()
        control.control_traffic()
        window.updatePos(aircraft.update_pos())

        
