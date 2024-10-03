# 3rd party modules
import locale
import logging

# Project modules
import commons
from LineWalker import LineWalker, PathData
from TennisCourt import TENNIS_COURT_HALF
from TennisCourt import TennisCourt
from TennisCourtDisplay import TennisCourtDisplay

USE_CACHE = True
DISPLAY_OPTIMIZED = True
DISPLAY_BEST_ONLY = True
DISPLAY_STEPS = False
DISPLAY_CANONICAL_PATH = False
DISPLAY_COURT = False
DISPLAY_LEGEND = False


class TennisCourtWipeOptimization:
    def __init__(
            self
    ):
        LOG_FILE_PATH = "../../../logs/"
        locale.setlocale(locale.LC_ALL, "german")
        commons.initialize(LOG_FILE_PATH)

        logging.debug("__init__()")

    def start(self):
        for id, tennisCourtLine in TENNIS_COURT_HALF.items():
            logging.debug("tennisCourtHalf: %s", tennisCourtLine)

        tennisCourt = TennisCourt()
        tennisCourtLineIndex: dict = tennisCourt.createTennisCourtLineIndex()

        tennisCourtDisplay = TennisCourtDisplay()

        if DISPLAY_COURT:
            tennisCourtDisplay.displayCourt(not DISPLAY_OPTIMIZED and not DISPLAY_CANONICAL_PATH)

        if DISPLAY_CANONICAL_PATH:
            lineWalker = LineWalker(tennisCourtLineIndex)
            canonicalPathData = lineWalker.walkCanonicalPathV3()

            if DISPLAY_STEPS:
                tennisCourtDisplay.displaySteps(canonicalPathData, False)
            tennisCourtDisplay.displayLines(canonicalPathData, not DISPLAY_OPTIMIZED)

        if DISPLAY_OPTIMIZED:
            startPointArray = [
                TENNIS_COURT_HALF["Sideline_Double_Back_Right"].start,
                TENNIS_COURT_HALF["Sideline_Double_Back_Right"].end,
                TENNIS_COURT_HALF["Sideline_Double_Front_Right"].end,
                TENNIS_COURT_HALF["Baseline_Single_Right"].end
            ]

            for startPointIndex, startPoint in enumerate(startPointArray, start=1):
                logging.debug("Starting with point %s", startPoint)

                lineWalker = LineWalker(tennisCourtLineIndex)
                filename = "optimzedPathDataArray-" + startPoint.normalize()

                optimzedPathDataArray = None
                if USE_CACHE:
                    logging.debug("Loading cache ...")

                    optimzedPathDataArray: list[PathData] = commons.restoreObject(filename)

                if optimzedPathDataArray is None:
                    logging.debug("Calculating optimized path ...")

                    optimzedPathDataArray: list[PathData] = lineWalker.calculateBestPaths(startPoint)

                    commons.storeObject(optimzedPathDataArray, filename)

                logging.debug("Optimized pathData: %s", optimzedPathDataArray)

                sortedOptimzedPathDataArray = sorted(optimzedPathDataArray, key=lambda x: x.getSortedIndex(),
                                                     reverse=False)

                if DISPLAY_BEST_ONLY:
                    if DISPLAY_STEPS:
                        tennisCourtDisplay.displaySteps(sortedOptimzedPathDataArray[0], False)
                    tennisCourtDisplay.displayLines(sortedOptimzedPathDataArray[0], DISPLAY_LEGEND,
                                                    startPointIndex == len(startPointArray))
                else:
                    for index, pathData in enumerate(sortedOptimzedPathDataArray, start=1):
                        if DISPLAY_STEPS:
                            tennisCourtDisplay.displaySteps(pathData, False)
                        tennisCourtDisplay.displayLines(pathData, DISPLAY_LEGEND,
                                                        startPointIndex == len(startPointArray))
