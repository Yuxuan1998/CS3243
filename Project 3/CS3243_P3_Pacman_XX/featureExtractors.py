# featureExtractors.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"Feature extractors for Pacman game states"

from game import Directions, Actions, Grid
import util

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state,action)] = 1.0
        return feats

class CoordinateExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closestFood(pos, food, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features

def closestItem(pos, itemGrid, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a item at this location then exit
        if itemGrid[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no item found
    return None

class NewExtractor(FeatureExtractor):
    """
    Design you own feature extractor here. You may define other helper functions you find necessary.
    """
    
    def getFeatures(self, state, action):
        "*** YOUR CODE HERE ***"
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()
        capsules = state.getCapsules()
        features = util.Counter()

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        not_scared_ghostsPosList = []
        not_scared_ghostsGrid = Grid(food.width, food.height)
        scared_ghostsPosList = []
        scared_ghostsGrid = Grid(food.width, food.height)

        features = util.Counter()

#        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        not_scared_ghostsPosList = []
        not_scared_ghostsGrid = Grid(food.width, food.height)
        scared_ghostsPosList = []
        scared_ghostsGrid = Grid(food.width, food.height)
        for i in range(len(ghosts)):
            if state.getGhostStates()[i].scaredTimer > 0.1:
                scared_ghostsPosList.append(ghosts[i])
                scared_ghostsGrid[int(ghosts[i][0])][int(ghosts[i][1])] = True
            else:
                not_scared_ghostsPosList.append(ghosts[i])
                not_scared_ghostsGrid[int(ghosts[i][0])][int(ghosts[i][1])] = True
        
        capsuleGrid = Grid(food.width, food.height)
        capsulePosList = []
        for i in range(len(capsules)):
            capsuleGrid[int(capsules[i][0])][int(capsules[i][1])] = True
            capsulePosList.append(capsules[i])

        if not_scared_ghostsGrid[next_x][next_y]:
            features["gets_eaten"] = 1.0
        features["#-of-not-scared-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        features["#-of-scared-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)

        features["#-of-not-scared-ghosts-2-steps-away"] = sum((next_x + 1, next_y) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x - 1, next_y) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x, next_y + 1) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x, next_y - 1) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)

        features["#-of-not-scared-ghosts-2-steps-away"] /= 4.0

        features["#-of-not-scared-ghosts-3-steps-away"] = sum((next_x, next_y + 2) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x, next_y - 2) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x + 1, next_y + 1) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x + 1, next_y - 1) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x - 1, next_y + 1) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x - 1, next_y - 1) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x + 2, next_y) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)
        + sum((next_x - 2, next_y) in Actions.getLegalNeighbors(g, walls) for g in not_scared_ghostsPosList)

        features["#-of-not-scared-ghosts-3-steps-away"] /= 8.0

        if features["#-of-not-scared-ghosts-1-step-away"] == 0:
            features["#-of-scared-ghosts-2-steps-away"] = sum((next_x + 1, next_y) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
            + sum((next_x - 1, next_y) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
            + sum((next_x, next_y + 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
            + sum((next_x, next_y - 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)

            features["#-of-scared-ghosts-2-steps-away"] /= 4.0

            if features["#-of-not-scared-ghosts-2-steps-away"] == 0:
                features["#-of-scared-ghosts-3-steps-away"] = sum((next_x, next_y + 2) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                + sum((next_x, next_y - 2) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                + sum((next_x + 1, next_y + 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                + sum((next_x + 1, next_y - 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                + sum((next_x - 1, next_y + 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                + sum((next_x - 1, next_y - 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                + sum((next_x + 2, next_y) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                + sum((next_x - 2, next_y) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)

                features["#-of-scared-ghosts-3-steps-away"] /= 8.0

                if features["#-of-not-scared-ghosts-3-steps-away"] == 0:
                    features["#-of-scared-ghosts-4-steps-away"] = sum((next_x, next_y + 3) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x, next_y - 3) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x + 1, next_y + 2) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x + 1, next_y - 2) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x - 1, next_y + 2) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x - 1, next_y - 2) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x + 2, next_y + 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x + 2, next_y - 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x - 2, next_y + 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x - 2, next_y - 1) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x + 3, next_y) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)
                    + sum((next_x - 3, next_y) in Actions.getLegalNeighbors(g, walls) for g in scared_ghostsPosList)

                    features["#-of-scared-ghosts-4-steps-away"] /= 12.0

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-not-scared-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0
        # if there is no danger of ghosts then add the capsule feature
        if not features["#-of-not-scared-ghosts-1-step-away"] and capsuleGrid[next_x][next_y]:
            features["eats-capsule"] = 1.0


        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features
