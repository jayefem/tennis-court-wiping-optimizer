# 3rd party modules
import logging

from Point import Point
from TennisCourtLine import TennisCourtLine


class TennisCourt:
    def __init__(
            self
    ):
        logging.debug("TennisCourt()")

    def createTennisCourtLineIndex(self):
        indexMap = {}

        for id, tennisCourtLine in TENNIS_COURT_HALF.items():
            # indexMap.get(tennisCourtLine.start, set()).add(tennisCourtLine)
            tennisCourtLineSet = indexMap.get(tennisCourtLine.start, set())
            tennisCourtLineSet.add(tennisCourtLine)
            indexMap[tennisCourtLine.start] = tennisCourtLineSet

            # indexMap.get(tennisCourtLine.end, set()).add(tennisCourtLine)
            tennisCourtLineSet = indexMap.get(tennisCourtLine.end, set())
            tennisCourtLineSet.add(tennisCourtLine)
            indexMap[tennisCourtLine.end] = tennisCourtLineSet

        logging.debug(indexMap)

        return indexMap


TENNIS_COURT_HALF = {
    "Baseline_Double_Right": TennisCourtLine(
        id="Baseline_Double_Right",
        name="Baseline Double Right",
        description="Baseline of the double corridor on the right of the player",
        start=Point(x=0.0, y=0.0),
        end=Point(x=0.0, y=1.37)
    ),
    "Baseline_Single_Right": TennisCourtLine(
        id="Baseline_Single_Right",
        name="Baseline Single Right",
        description="Baseline of the single court on the right of the player",
        start=Point(x=0.0, y=1.37),
        end=Point(x=0.0, y=1.37 + 4.115)
    ),
    "Baseline_Single_Left": TennisCourtLine(
        id="Baseline_Single_Left",
        name="Baseline Single Left",
        description="Baseline of the single court on the left of the player",
        start=Point(x=0.0, y=1.37 + 4.115),
        end=Point(x=0.0, y=9.6)  # y=1.37+4.115+4.115
    ),
    "Baseline_Double_Left": TennisCourtLine(
        id="Baseline_Double_Left",
        name="Baseline Double Left",
        description="Baseline of the double corridor on the left of the player",
        start=Point(x=0.0, y=9.6),  # y=1.37+4.115+4.115
        end=Point(x=0.0, y=10.97)  # y=1.37+4.115+4.115+1.37
    ),

    "Sideline_Double_Back_Right": TennisCourtLine(
        id="Sideline_Double_Back_Right",
        name="Sideline Double Back Right",
        description="Double sideline from the baseline to the T-line on the right of the player",
        start=Point(x=0.0, y=0.0),
        end=Point(x=5.485, y=0.0)
    ),
    "Sideline_Double_Back_Left": TennisCourtLine(
        id="Sideline_Double_Back_Left",
        name="Sideline Double Back Left",
        description="Double sideline from the baseline to the T-line on the left of the player",
        start=Point(x=0.0, y=10.97),  # y=1.37+4.115+4.115+1.37,
        end=Point(x=5.485, y=10.97)  # y=1.37+4.115+4.115+1.37
    ),
    "Sideline_Double_Front_Right": TennisCourtLine(
        id="Sideline_Double_Front_Right",
        name="Sideline Double Front Right",
        description="Double sideline from the T-line to the net on the right of the player",
        start=Point(x=5.485, y=0.0),
        end=Point(x=11.885, y=0.0)  # x=5.485+6.40
    ),
    "Sideline_Double_Front_Left": TennisCourtLine(
        id="Sideline_Double_Front_Left",
        name="Sideline Double Front Left",
        description="Double sideline from the T-line to the net on the left of the player",
        start=Point(x=5.485, y=10.97),  # y=1.37+4.115+4.115+1.37,
        end=Point(x=11.885, y=10.97)  # x=5.485+6.40, y=1.37+4.115+4.115+1.37
    ),

    "Sideline_Single_Back_Right": TennisCourtLine(
        id="Sideline_Single_Back_Right",
        name="Sideline Single Back Right",
        description="Single sideline from the baseline to the T-line on the right of the player",
        start=Point(x=0.0, y=1.37),
        end=Point(x=5.485, y=1.37)
    ),
    "Sideline_Single_Back_Left": TennisCourtLine(
        id="Sideline_Single_Back_Left",
        name="Sideline Single Back Left",
        description="Single sideline from the baseline to the T-line on the left of the player",
        start=Point(x=0.0, y=9.6),  # y=1.37+4.115+4.115,
        end=Point(x=5.485, y=9.6)  # y=1.37+4.115+4.115
    ),
    "Sideline_Single_Front_Right": TennisCourtLine(
        id="Sideline_Single_Front_Right",
        name="Sideline Single Front Right",
        description="Single sideline from the T-line to the net on the right of the player",
        start=Point(x=5.485, y=1.37),
        end=Point(x=11.885, y=1.37)  # x=5.485+6.40
    ),
    "Sideline_Single_Front_Left": TennisCourtLine(
        id="Sideline_Single_Front_Left",
        name="Sideline Single Front Left",
        description="Single sideline from the T-line to the net on the left of the player",
        start=Point(x=5.485, y=9.6),  # y=1.37+4.115+4.115,
        end=Point(x=11.885, y=9.6)  # x=5.485+6.40, y=1.37+4.115+4.115
    ),
    "T_Line_Right": TennisCourtLine(
        id="T_Line_Right",
        name="T-Line Right",
        description="T-Line on the right of the player",
        start=Point(x=5.485, y=1.37),
        end=Point(x=5.485, y=1.37 + 4.115)
    ),
    "T_Line_Left": TennisCourtLine(
        id="T_Line_Left",
        name="T-Line Left",
        description="T-Line on the left of the player",
        start=Point(x=5.485, y=1.37 + 4.115),
        end=Point(x=5.485, y=9.6)  # 1.37+4.115+4.115
    ),
    "Middleline": TennisCourtLine(
        id="Middleline",
        name="Middleline",
        description="Middleline",
        start=Point(x=5.485, y=1.37 + 4.115),
        end=Point(x=11.885, y=1.37 + 4.115)  # x=5.485+6.40
    )
}
