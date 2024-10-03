# 3rd party modules
import copy
import logging
from collections import Counter
from typing import List

# Project modules
from Point import Point
from TennisCourt import TENNIS_COURT_HALF
from TennisCourtLine import TennisCourtLine

CANONICAL_PATH = [
    TENNIS_COURT_HALF["Sideline_Double_Back_Right"].start,
    TENNIS_COURT_HALF["Sideline_Double_Front_Right"].start,
    TENNIS_COURT_HALF["Sideline_Double_Front_Right"].end,
    TENNIS_COURT_HALF["Sideline_Single_Front_Right"].end,
    TENNIS_COURT_HALF["Sideline_Single_Back_Right"].end,
    TENNIS_COURT_HALF["Sideline_Single_Back_Right"].start,
    TENNIS_COURT_HALF["Baseline_Double_Right"].start,
    TENNIS_COURT_HALF["Baseline_Single_Right"].start,
    TENNIS_COURT_HALF["Baseline_Single_Left"].start,
    TENNIS_COURT_HALF["Baseline_Double_Left"].start,
    TENNIS_COURT_HALF["Sideline_Double_Back_Left"].start,
    TENNIS_COURT_HALF["Sideline_Double_Front_Left"].start,
    TENNIS_COURT_HALF["Sideline_Double_Front_Left"].end,
    TENNIS_COURT_HALF["Sideline_Single_Front_Left"].end,
    TENNIS_COURT_HALF["Sideline_Single_Front_Left"].start,
    TENNIS_COURT_HALF["Sideline_Single_Back_Left"].start,
    TENNIS_COURT_HALF["T_Line_Left"].end,
    TENNIS_COURT_HALF["T_Line_Left"].start,
    TENNIS_COURT_HALF["Middleline"].end,
    TENNIS_COURT_HALF["T_Line_Right"].end,
    TENNIS_COURT_HALF["T_Line_Right"].start,
    # Back to the beginning
    TENNIS_COURT_HALF["Sideline_Double_Back_Right"].start
]

CANONICAL_PATH_V2 = [
    TENNIS_COURT_HALF["Sideline_Double_Front_Right"].end,
    TENNIS_COURT_HALF["Sideline_Double_Front_Right"].start,
    TENNIS_COURT_HALF["Sideline_Double_Back_Right"].start,
    TENNIS_COURT_HALF["Baseline_Double_Right"].end,
    TENNIS_COURT_HALF["Sideline_Single_Back_Right"].end,
    TENNIS_COURT_HALF["Sideline_Single_Front_Right"].end,
    TENNIS_COURT_HALF["Middleline"].end,
    TENNIS_COURT_HALF["T_Line_Right"].end,
    TENNIS_COURT_HALF["T_Line_Right"].start,
    TENNIS_COURT_HALF["T_Line_Right"].end,
    TENNIS_COURT_HALF["T_Line_Left"].end,
    TENNIS_COURT_HALF["Sideline_Single_Front_Left"].end,
    TENNIS_COURT_HALF["Sideline_Double_Front_Left"].end,
    TENNIS_COURT_HALF["Sideline_Double_Front_Left"].start,
    TENNIS_COURT_HALF["Sideline_Double_Back_Left"].start,
    TENNIS_COURT_HALF["Baseline_Double_Left"].start,
    TENNIS_COURT_HALF["Sideline_Single_Back_Left"].end,
    TENNIS_COURT_HALF["Sideline_Single_Back_Left"].start,
    TENNIS_COURT_HALF["Baseline_Single_Left"].start,
    TENNIS_COURT_HALF["Baseline_Single_Right"].start,

    # Back to the beginning
    TENNIS_COURT_HALF["Sideline_Double_Front_Right"].end,
]

CANONICAL_PATH_V3 = [
    TENNIS_COURT_HALF["Sideline_Double_Front_Right"].end,
    TENNIS_COURT_HALF["Sideline_Double_Front_Right"].start,
    TENNIS_COURT_HALF["Sideline_Double_Back_Right"].start,
    TENNIS_COURT_HALF["Baseline_Double_Right"].end,
    TENNIS_COURT_HALF["Sideline_Single_Back_Right"].end,
    TENNIS_COURT_HALF["Sideline_Single_Front_Right"].end,
    TENNIS_COURT_HALF["T_Line_Right"].start,
    TENNIS_COURT_HALF["T_Line_Right"].end,
    TENNIS_COURT_HALF["Middleline"].end,
    TENNIS_COURT_HALF["T_Line_Right"].end,
    TENNIS_COURT_HALF["T_Line_Left"].end,
    TENNIS_COURT_HALF["Sideline_Single_Front_Left"].end,
    TENNIS_COURT_HALF["Sideline_Double_Front_Left"].end,
    TENNIS_COURT_HALF["Sideline_Double_Front_Left"].start,
    TENNIS_COURT_HALF["Sideline_Double_Back_Left"].start,
    TENNIS_COURT_HALF["Baseline_Double_Left"].start,
    TENNIS_COURT_HALF["Sideline_Single_Back_Left"].end,
    TENNIS_COURT_HALF["Sideline_Single_Back_Left"].start,
    TENNIS_COURT_HALF["Baseline_Single_Left"].start,
    TENNIS_COURT_HALF["Baseline_Single_Right"].start,

    # Back to the beginning
    TENNIS_COURT_HALF["Sideline_Double_Front_Right"].end,
]



MAX_WIPE_NUMBER = 2
MAX_VISIT_NUMBER = 2
MAX_STEP_NUMBER = len(CANONICAL_PATH) + 1
MIN_PATH_LENGTH = sum([tennisCourtLine.length() for id, tennisCourtLine in TENNIS_COURT_HALF.items()])


class PathItem:
    def __init__(
            self,
            point: Point,
            wiped: TennisCourtLine
    ):
        self.point = point
        self.wiped = wiped

    def __hash__(self):
        return hash(f"{self.point}")

    def __eq__(self, other):
        return self.point == other.point

    def __repr__(self):
        return f"({self.point}, {self.wiped})"


class PathData:
    def __init__(
            self,
            name
    ):

        logging.debug("PathData.init()")

        self.name = name

        self.opimizedVersion = 0
        self.path: list[PathItem] = []
        self.pathLength = 0.0
        self.lastStepLength = 0.0
        self.wipedMap = {}
        self.indexArray: list[int] = []

    def isFinished(self):
        return len(self.wipedMap) == len(TENNIS_COURT_HALF)

    def goStepBack(self):
        if len(self.indexArray) != len(self.path):
            logging.warning("len(self.indexArray) != len(self.path): %i != %i", len(self.indexArray), len(self.path))

        if len(self.indexArray) > 0:
            self.indexArray.pop()

        if len(self.path) == 0:
            return

        currentPathItem = self.path.pop()
        pathArrayLength = len(self.path)
        if pathArrayLength > 0:
            previousPoint: Point = self.path[pathArrayLength - 1].point
            self.pathLength -= previousPoint.distance(currentPathItem.point)
            # lastStepLength => not defined
            self.lastStepLength = -1

            if currentPathItem.wiped in self.wipedMap:
                self.wipedMap[currentPathItem.wiped] -= 1
                if self.wipedMap[currentPathItem.wiped] <= 0:
                    del self.wipedMap[currentPathItem.wiped]

    def getPathLengthCalculated(self):
        previousItem = None
        length = 0.0
        for pathItem in self.path:
            if previousItem is not None:
                length += previousItem.point.distance(pathItem.point)

            previousItem = pathItem

        return length

    def getNumberOfSteps(self):
        return len(self.path)

    def getNumberOfDirectionChanges(self):
        numberOfDirectionChanges = 0
        for index, pathItem in enumerate(self.path, start=0):
            if index < 2:
                continue

            if pathItem.point.x != self.path[index - 2].point.x and pathItem.point.y != self.path[index - 2].point.y:
                numberOfDirectionChanges += 1

        return numberOfDirectionChanges

    def getSortedIndex(self):
        return 1000 * self.pathLength + self.getNumberOfDirectionChanges()

    def __repr__(self):
        return f"PathData '{self.name}', opimizedVersion: {self.opimizedVersion}, pathLength: {self.pathLength}, lastStepLength: {self.lastStepLength}, No. of steps: {len(self.path)}, wipedMap: {self.wipedMap}, indexArray: {self.indexArray}"


class LineWalker:
    def __init__(
            self,
            tennisCourtLineIndex: dict
    ):

        logging.debug("LineWalker.init()")

        self.tennisCourtLineIndex = tennisCourtLineIndex

        self.optimzedPathDataArray = []

        self.counter: int = 0
        self.pruneCounter: int = 0

    def walkCanonicalPath(self):
        return self.walkThePath("Canonical path", CANONICAL_PATH)

    def walkCanonicalPathV2(self):
        return self.walkThePath("Canonical path", CANONICAL_PATH_V2)

    def walkCanonicalPathV3(self):
        return self.walkThePath("Canonical path", CANONICAL_PATH_V3)

    def getIndexByPoint(self, point: Point):
        return list(self.tennisCourtLineIndex.keys()).index(point)

    def calculateBestPaths(self, start: Point):
        logging.debug("calculateBestPath() - Starting with: %s", start)

        # Init maximumPathLength with canonical path
        canonicalPathData: PathData = self.walkCanonicalPath()
        self.optimzedPathDataArray.append(canonicalPathData)

        logging.info("calculateBestPath() - Initial canonicalPathData: %s", canonicalPathData)

        pathData: PathData = PathData("Init path")
        pathData.indexArray.append(self.getIndexByPoint(start))
        self.calculateBestPathRecursive(start, pathData)

        return self.optimzedPathDataArray

    def calculateBestPathRecursive(self, to: Point, pathData: PathData):
        if self.counter % 200000 == 0:
            steps: int = len(pathData.path)
            optimzedPathData: PathData = self.optimzedPathDataArray[-1]
            logging.info(
                "calculateBestPathRecursive() - Optimized version %s, Optimized steps %i, Optimized length %s, counter: %i, pruneCounter: %s, indexArray: %s, steps: %i",
                optimzedPathData.opimizedVersion, optimzedPathData.getNumberOfSteps(), optimzedPathData.pathLength,
                self.counter, self.pruneCounter, pathData.indexArray, steps)

        self.counter += 1

        pathData = self.walkTheLine(to, pathData)

        if self.prunePath(pathData):
            self.pruneCounter += 1
            # Clean up data before recursion. Otherwise, maximum recursion depth exceeded because Python lacks the tail recursion optimizations.
            pathData.goStepBack()

            return pathData

        # Found candidate
        if pathData.isFinished():
            # Go back to the beginning
            startPoint = pathData.path[0].point
            currentPoint = pathData.path[-1].point

            if startPoint != currentPoint:
                logging.trace(
                    "calculateBestPathRecursive() - Found a new optimized path but there's still one step left to the starting point! %s",
                    pathData)

                pathData.indexArray.append(self.getIndexByPoint(startPoint))
                pathData = self.calculateBestPathRecursive(startPoint, pathData)
            else:
                pathData.opimizedVersion += 1

                newOptimzedPathData: PathData = copy.deepcopy(pathData)
                newOptimzedPathData.name = f'Optimized path v{pathData.opimizedVersion}'

                logging.info("calculateBestPath() - FOUND new optimized path! %s", newOptimzedPathData)

                self.optimzedPathDataArray.append(newOptimzedPathData)

            # Clean up data before recursion. Otherwise, maximum recursion depth exceeded because Python lacks the tail recursion optimizations.
            pathData.goStepBack()

            return pathData

        for index, point in enumerate(self.tennisCourtLineIndex):
            currentPoint: Point = pathData.path[len(pathData.path) - 1].point

            if point == currentPoint:
                continue

            pathData.indexArray.append(index)

            pathData = self.calculateBestPathRecursive(point, pathData)

            # Do not call any command after the recursive call in the loop.
            # Otherwise, the error "maximum recursion depth exceeded while calling a Python object" occurs

        pathData.goStepBack()

        return pathData

    def prunePath(self, pathData: PathData):
        steps: int = len(pathData.path)
        optimzedPathData: PathData = self.optimzedPathDataArray[-1]

        if pathData.pathLength > optimzedPathData.pathLength:
            logging.trace("calculateBestPathRecursive() - prune - path length is longer than the optimized path: %s",
                          optimzedPathData.pathLength)

            return True

        if len(pathData.wipedMap) > 0:
            if pathData.path[-1].wiped != None:
                if pathData.wipedMap[pathData.path[-1].wiped] > MAX_WIPE_NUMBER:
                    logging.trace(
                        "calculateBestPathRecursive() - prune - one line was more often wiped than reasonable (more than MAX_WIPE_NUMBER times): %s",
                        pathData.wipedMap[list(pathData.wipedMap.keys())[-1]])

                    return True

        if len(pathData.path) > 1:
            if pathData.path[-1].wiped == None and pathData.path[-2].wiped == None:
                logging.trace(
                    "calculateBestPathRecursive() - prune - visiting two points in a row without wiping is not reasonable.")

                return True

        if steps > MAX_STEP_NUMBER:
            logging.trace("calculateBestPathRecursive() - prune - more steps than the canonical path + buffer: %s",
                          len(pathData.path))

            return True

        if Counter(pathData.path).most_common(1)[0][1] > MAX_VISIT_NUMBER:
            logging.trace(
                "calculateBestPathRecursive() - prune - one point was visited more than MAX_VISIT_NUMBER times: %s",
                MAX_VISIT_NUMBER + 1)

            return True

        # Calculate lines which are not yet wiped (intersect all lines with already wiped lines)
        restPath: list[TennisCourtLine] = list(set(TENNIS_COURT_HALF.values()) - set(pathData.wipedMap.keys()))
        # Calculate path lenght of all lines which were not wiped yet
        minimumRestPathLength = sum([tennisCourtLine.length() for tennisCourtLine in restPath])
        if pathData.pathLength + minimumRestPathLength > optimzedPathData.pathLength:
            logging.trace(
                "calculateBestPathRecursive() - prune - current path length (%s) + minimum rest path length (%s) is already longer than the optimized path: %s",
                pathData.pathLength, minimumRestPathLength, pathData.pathLength + minimumRestPathLength)

            return True

        return False

    def walkThePath(self, name: str, walkingPath: List[Point]):
        logging.debug("walkThePath()")

        pathData: PathData = PathData(name)

        for to in walkingPath:
            self.walkTheLine(to, pathData)

        startPoint = pathData.path[0].point
        currentPoint = pathData.path[-1].point

        if startPoint != currentPoint:
            self.walkTheLine(startPoint, pathData)

        pathData.lastStepLength = startPoint.distance(currentPoint)

        logging.debug("walkThePath() - length: %s, len(pathData.path): %d", pathData.pathLength,
                      len(pathData.path))

        return pathData

    def walkTheLine(self, to: Point, pathData: PathData):
        logging.trace("walkTheLine() - to %s", to)

        tennisCourtLine = None

        pathArrayLength = len(pathData.path)
        if pathArrayLength > 0:
            previousPoint: Point = pathData.path[pathArrayLength - 1].point

            if previousPoint == to:
                logging.warning("walkTheLine() - Can't walk to the same point: %s", previousPoint)
                return pathData

            distance = previousPoint.distance(to)
            pathData.pathLength += distance
            pathData.lastStepLength = distance

            tennisCourtLineIntersect = self.tennisCourtLineIndex[previousPoint] & self.tennisCourtLineIndex[to]

            if len(tennisCourtLineIntersect) > 0:
                if len(tennisCourtLineIntersect) > 1:
                    logging.warning("walkTheLine() - tennisCourtLineIntersect has more than 1 item! set: %s",
                                    tennisCourtLineIntersect)

                tennisCourtLine = list(tennisCourtLineIntersect)[0]
                logging.trace("walkTheLine() - is wiped: %s", tennisCourtLine)

                if tennisCourtLine in pathData.wipedMap:
                    pathData.wipedMap[tennisCourtLine] += 1
                else:
                    pathData.wipedMap[tennisCourtLine] = 1

        pathData.path.append(PathItem(to, tennisCourtLine))

        return pathData
