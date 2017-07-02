import yaml
import specification
from nusmvbdr import ExpressionBuilder, ExpressionDefinitionBuilder, CaseDefinitionBuilder
import movement


def genmodel(in_file, out_file):
    specstream = open(in_file, "r")
    specs = yaml.safe_load(specstream)

    modelstream = open(out_file, "w")

    worldspec = specification.WorldSpec(specs["world"])
    islandspec = specification.IslandSpec(specs["island"])
    penguinspec = specification.PenguinSpec(specs["penguin"])
    snowballspec = specification.SnowballSpec(specs["snowball"])

    sbdefs = sbdefinitions(worldspec, islandspec, penguinspec, snowballspec)
    pgdefs = pgdefinitions(worldspec, islandspec, penguinspec, snowballspec)

    modelstream.write("// Snowball definitions\n\n")
    modelstream.write('\n\n'.join(list(map(lambda x: x.build(), sbdefs))))

    modelstream.write("\n\n// Penguin definitions\n\n")
    modelstream.write('\n\n'.join(list(map(lambda x: x.build(), pgdefs))))


def sbdefinitions(worldspec, islandspec, penguinspec, snowballspec):
    definitions = []

    flies = movement.moves(snowballspec.flyvel)
    definitions.append(movecase(flies, "FlightPosChanged"))
    definitions.append(coldetecteddf(penguinspec.radius, snowballspec.radius, "CollisionDetected"))
    definitions.append(sbdeadptsdefs(islandspec, snowballspec))

    return definitions

def sbdeadptsdefs(islandspec, snowballspec):
    containsfunc = lambda point: islandspec.contains(point)
    combineddpts = deadpoints([snowballspec.flyvel], islandspec.centerx, islandspec.centery, islandspec.bradius,
                              islandspec.sradius, containsfunc)
    return deadptsdef(combineddpts, "DeadPointReached")

def pgdefinitions(worldspec, islandspec, penguinspec, snowballspec):
    definitions = []

    moves = movement.moves(penguinspec.movevel)
    definitions.append(moveexp(moves, "MovePosChanged"))

    pngvels = movement.fricvelext(penguinspec.mass, islandspec.friction, penguinspec.pngvel, 1)

    if penguinspec.movevel in pngvels:
        possiblevels = pngvels
    else:
        possiblevels = pngvels[1:] + [penguinspec.movevel]

    definitions.append(ExpressionDefinitionBuilder("d_pushing_index_max", ExpressionBuilder(len(pngvels)-1).build()))
    definitions.append(pgpushingdef(penguinspec, pngvels))
    definitions.append(pgsbinitdef(penguinspec))
    definitions.append(pngdeadptsdef(islandspec, possiblevels))
    definitions.append(coldetecteddf(penguinspec.radius, penguinspec.radius, "CollisionDetected"))

    return definitions

def pgpushingdef(penguinspec, pngvels):
    pngmovecase = CaseDefinitionBuilder("PushingPosChanged")
    pngindexp = ExpressionBuilder("pushing_index")
    expconj = lambda exp1, exp2: exp1.withand(exp2)
    for pngind in range(1, len(pngvels)):
        pngmoves = movement.moves(pngvels[pngind])

        casedef = movecase(pngmoves, pngmovecase.name())
        casedef = casedef.withexpappended(pngindexp.witheq(ExpressionBuilder(pngind)), expconj)
        pngmovecase = pngmovecase.combined(casedef)

    return pngmovecase


def pgsbinitdef(penguinspec):
    casedef = CaseDefinitionBuilder("SnowballInit")
    direxp = ExpressionBuilder("snowball.direction").withnext()
    nxexp = ExpressionBuilder("snowball.x").withnext().withsub(ExpressionBuilder("x")).withparen()
    nyexp = ExpressionBuilder("snowball.y").withnext().withsub(ExpressionBuilder("y")).withparen()

    offsets = movement.pointrot(penguinspec.sbox, penguinspec.sboy)
    direction = 0
    for i in range(1, len(offsets) + 1):
        if i == len(offsets) or offsets[direction] != offsets[i]:
            if direction - i > 1:
                exp = direxp.within(ExpressionBuilder(direction, i-1))
            else:
                exp = direxp.witheq(ExpressionBuilder(direction))

            exp = exp.withand(nxexp.witheq(ExpressionBuilder(offsets[direction][0])))
            exp = exp.withand(nyexp.witheq(ExpressionBuilder(offsets[direction][1])))

            casedef = casedef.withcase(exp.build(), ExpressionBuilder.true().build())
            direction = i

    casedef = casedef.withcase(ExpressionBuilder.true().build(), ExpressionBuilder.false().build())
    return casedef


def pngdeadptsdef(islandspec, velocities):
    containsfunc = lambda point: islandspec.contains(point)
    combineddpts = deadpoints(velocities, islandspec.centerx, islandspec.centery, islandspec.bradius,
                              islandspec.sradius, containsfunc)
    return deadptsdef(combineddpts, "DeadPointReached")

def deadptsdef(combinedpts, name):
    casedef = CaseDefinitionBuilder(name)
    nexpx = ExpressionBuilder("x").withnext()
    nexpy = ExpressionBuilder("y").withnext()

    for x, yList in combinedpts.items():
        base = 0
        for i in range(1, len(yList) + 1):
            if i == len(yList) or yList[i] - yList[i - 1] > 1:
                expx = nexpx.witheq(ExpressionBuilder(x))
                if i - base > 1:
                    expy = nexpy.within(ExpressionBuilder(yList[base], yList[i - 1]))
                else:
                    expy = nexpy.witheq(ExpressionBuilder(yList[i - 1]))

                casedef = casedef.withcase(expx.withand(expy).build(), ExpressionBuilder.true().build())
                base = i

    casedef = casedef.withcase(ExpressionBuilder.true().build(), ExpressionBuilder.false().build())

    return casedef

def coldetecteddf(srcrad, destrad, name):
    colradius = srcrad + destrad

    casedef = CaseDefinitionBuilder(name)
    xexp = ExpressionBuilder("x")
    yexp = ExpressionBuilder("y")
    nexpx = xexp.withnext().withsub(xexp).withparen()
    nexpy = yexp.withnext().withsub(yexp).withparen()
    offsets = {}
    for x in range(-colradius, colradius + 1):
        for y in range(-colradius, colradius + 1):
            if x * x + y * y <= colradius * colradius:
                if x not in offsets:
                    offsets[x] = []
                offsets[x].append(y)

    for x, yList in offsets.items():
        base = 0
        for i in range(1, len(yList) + 1):
            if i == len(yList) or yList[i] - yList[i - 1] != 1:
                expx = nexpx.witheq(ExpressionBuilder(x))
                if i - base > 1:
                    expy = nexpy.within(ExpressionBuilder(yList[base], yList[i - 1]))
                else:
                    expy = nexpy.witheq(ExpressionBuilder(yList[i - 1]))

                casedef = casedef.withcase(expx.withand(expy).build(), ExpressionBuilder.true().build())
                base = i

    casedef = casedef.withcase(ExpressionBuilder.true().build(), ExpressionBuilder.false().build())

    return casedef

def deadpoints(velocities, centerX, centerY, hrad, vrad, containsfunc):
    veldic = {}
    dpoints = []

    for v in velocities:
        moves = movement.moves(v)
        moves = list(filter(lambda p: p[0] <= 0 and p[1] <= 0, moves))
        veldic[v] = moves

    for ix in range(centerX - hrad, centerX + 1):
        for iy in range(centerY - vrad, centerY + 1):
            for v, moves in veldic.items():
                for ox, oy in moves:
                    if containsfunc((ix, iy)) and not containsfunc((ix + ox, iy + oy)):
                        dpoints.append((ix + ox, iy + oy))

                        if 2*centerX - ix - ox != ix + ox:
                            dpoints.append((2 * centerX - ix - ox, iy + oy))

                        if 2*centerY - iy - oy != iy + oy:
                            dpoints.append((ix + ox, 2 * centerY - iy - oy))

                        if 2*centerX - ix - ox != ix + ox and 2*centerY - iy - oy != iy + oy:
                            dpoints.append((2 * centerX - ix - ox, 2 * centerY - iy - oy))

    return combinepoints(dpoints)

def moveexp(points, name):
    fullexp = None
    direxp = ExpressionBuilder("direction")
    xexp = ExpressionBuilder("x")
    yexp = ExpressionBuilder("y")
    nextxexp = xexp.withnext().withsub(xexp).withparen()
    nextyexp = yexp.withnext().withsub(yexp).withparen()

    direction = 0
    for i in range(1, len(points) + 1):
        if i == len(points) or points[i][0] != points[direction][0] or points[i][1] != points[direction][1]:
            if (i - direction) > 1:
                expression = direxp.within(ExpressionBuilder(direction, i-1))
            else:
                expression = direxp.witheq(ExpressionBuilder(direction))

            expression = expression.withand(nextxexp.witheq(ExpressionBuilder(points[direction][0])))
            expression = expression.withand(nextyexp.witheq(ExpressionBuilder(points[direction][1])))

            if fullexp is None:
                fullexp = expression
            else:
                fullexp = fullexp.withnewline().withor(expression)

            direction = i

    return ExpressionDefinitionBuilder(name).withexp(fullexp.build())


def movecase(points, name):
    casebdr = CaseDefinitionBuilder(name)
    direxp = ExpressionBuilder("direction")
    xexp = ExpressionBuilder("x")
    yexp = ExpressionBuilder("y")
    nextxexp = xexp.withnext().withsub(xexp).withparen()
    nextyexp = yexp.withnext().withsub(yexp).withparen()

    direction = 0
    for i in range(1, len(points) + 1):
        if i == len(points) or points[i] != points[direction]:
            if (i - direction) > 1:
                expression = direxp.within(ExpressionBuilder(direction, i-1))
            else:
                expression = direxp.witheq(ExpressionBuilder(direction))

            expression = expression.withand(nextxexp.witheq(ExpressionBuilder(points[direction][0])))
            expression = expression.withand(nextyexp.witheq(ExpressionBuilder(points[direction][1])))

            casebdr = casebdr.withcase(expression.build(), ExpressionBuilder.true().build())
            direction = i

    casebdr = casebdr.withcase(ExpressionBuilder.true().build(), ExpressionBuilder.false().build())

    return casebdr

def combinepoints(points):
    pointsdic = {}
    for x, y in points:
        if x not in pointsdic:
            pointsdic[x] = []
        if y not in pointsdic[x]:
            pointsdic[x].append(y)

    for x in pointsdic.keys():
        pointsdic[x] = sorted(pointsdic[x])

    return pointsdic
