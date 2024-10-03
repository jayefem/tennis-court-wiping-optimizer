# 3rd party modules
import logging

# Project modules
from LineWalker import PathData
from src.main.python.TennisCourt import TENNIS_COURT_HALF

logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('matplotlib.pyplot').setLevel(logging.WARNING)
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.WARNING)
import matplotlib.pyplot as plt


class TennisCourtDisplay:
    def __init__(
            self
    ):
        logging.debug("__init__()")

    def displayLines(self, pathData: PathData, displayLegend: bool = True, show: bool = False):
        startPoint = pathData.path[0].point
        title = "Start at=" + startPoint.__str__() + "\n" + pathData.name + "\nPath length=" + str(
            "%.2f" % pathData.pathLength) + "\nNumber of steps=" + str(
            len(pathData.path)) + "\nNumber of direction changes=" + str(pathData.getNumberOfDirectionChanges())

        tennisCourtLineMap = pathData.wipedMap

        # Visualization with Matplotlib
        plt.figure(figsize=(6, 12))

        # Draw lines
        for index, tennisCourtLine in enumerate(tennisCourtLineMap, start=1):
            x_values = [tennisCourtLine.start.x, tennisCourtLine.end.x]
            y_values = [tennisCourtLine.start.y, tennisCourtLine.end.y]
            plt.plot(x_values, y_values, label=tennisCourtLine.name + " (" + str(index) + ")")

            # Calculation of center of the line for the label
            mid_x = (tennisCourtLine.start.x + tennisCourtLine.end.x) / 2
            mid_y = (tennisCourtLine.start.y + tennisCourtLine.end.y) / 2

            # Place label in the center of line
            plt.text(mid_x, mid_y, str(index), fontsize=10, ha='center', va='center', backgroundcolor='w')

        # Place "X" at the starting point
        plt.text(startPoint.x, startPoint.y, "X", fontsize=12, color='red', ha='center', va='center')

        # Tenniscourt adaption (length/width)
        plt.xlim(-1, TENNIS_COURT_HALF["Sideline_Double_Back_Left"].start.distance(
            TENNIS_COURT_HALF["Sideline_Double_Front_Left"].end))  # Platz für Ränder
        if displayLegend:
            plt.ylim(-1, 23)
        else:
            plt.ylim(-1, 12)

        # Additional options for better display
        plt.gca().set_aspect('equal', adjustable='box')  # Gleiche Skalierung der Achsen
        plt.title(title)
        plt.xlabel("Width (m)")
        plt.ylabel("Length (m)")
        plt.grid(True)

        # Show legend
        if displayLegend:
            plt.legend()

        # Plot lines
        if show:
            plt.show()

    def displaySteps(self, pathData: PathData, show: bool = False):
        startPoint = pathData.path[0].point
        title = "Start at=" + startPoint.__str__() + "\n" + pathData.name + " (steps)\nPath length=" + str(
            "%.2f" % pathData.pathLength) + "\nNumber of steps=" + str(
            len(pathData.path)) + "\nNumber of direction changes=" + str(pathData.getNumberOfDirectionChanges())

        # Visualization with Matplotlib
        plt.figure(figsize=(6, 12))

        # Draw lines
        previousPathItem = None
        for index, pathItem in enumerate(pathData.path, start=0):
            if previousPathItem is not None:
                x_values = [previousPathItem.point.x, pathItem.point.x]
                y_values = [previousPathItem.point.y, pathItem.point.y]
                plt.plot(x_values, y_values, label=str(index))

                # Calculation of center of the line for the label
                mid_x = (previousPathItem.point.x + pathItem.point.x) / 2
                mid_y = (previousPathItem.point.y + pathItem.point.y) / 2

                # Place label in the center of line
                plt.text(mid_x, mid_y, str(index), fontsize=10, ha='center', va='center', backgroundcolor='w')

            previousPathItem = pathItem

        # Place "X" at the starting point
        plt.text(startPoint.x, startPoint.y, "X", fontsize=12, color='red', ha='center', va='center')

        # Tenniscourt adaption (length/width)
        plt.xlim(-1, TENNIS_COURT_HALF["Sideline_Double_Back_Left"].start.distance(
            TENNIS_COURT_HALF["Sideline_Double_Front_Left"].end))  # Platz für Ränder
        plt.ylim(-1, 12)

        # Additional options for better display
        plt.gca().set_aspect('equal', adjustable='box')  # Gleiche Skalierung der Achsen
        plt.title(title)
        plt.xlabel("Width (m)")
        plt.ylabel("Length (m)")
        plt.grid(True)

        # Plot lines
        if show:
            plt.show()

    def displayCourt(self, show: bool = False):
        title = "Tennis court dimensions"

        # Visualization with Matplotlib
        plt.figure(figsize=(6, 12))

        # Draw lines
        for key, tennisCourtLine in TENNIS_COURT_HALF.items():
            distance = tennisCourtLine.start.distance(tennisCourtLine.end)
            x_values = [tennisCourtLine.start.x, tennisCourtLine.end.x]
            y_values = [tennisCourtLine.start.y, tennisCourtLine.end.y]
            plt.plot(x_values, y_values, label=tennisCourtLine.name + " (" + str("%.3f" % distance) + " m)")

            # Calculation of center of the line for the label
            mid_x = (tennisCourtLine.start.x + tennisCourtLine.end.x) / 2
            mid_y = (tennisCourtLine.start.y + tennisCourtLine.end.y) / 2

            # Place label in the center of line
            plt.text(mid_x, mid_y, str("%.3f" % distance) + " m", fontsize=10,
                     ha='center', va='center', backgroundcolor='w')

        # Tenniscourt adaption (length/width)
        plt.xlim(-1, TENNIS_COURT_HALF["Sideline_Double_Back_Left"].start.distance(
            TENNIS_COURT_HALF["Sideline_Double_Front_Left"].end))  # Platz für Ränder
        plt.ylim(-1, 23)

        # Additional options for better display
        plt.gca().set_aspect('equal', adjustable='box')  # Gleiche Skalierung der Achsen
        plt.title(title)
        plt.xlabel("Width (m)")
        plt.ylabel("Length (m)")
        plt.grid(True)

        plt.legend()

        # Plot lines
        if show:
            plt.show()
