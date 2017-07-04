import yaml
import specification
from nusmvbdr import ExpressionBuilder, ExpressionDefinitionBuilder, CaseDefinitionBuilder
import movement
import math

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
    collision_offsets = collisionoffsets(penguinspec.radius, penguinspec.pngvel, snowballspec.radius, snowballspec.flyvel)
    definitions.append(coldetecteddf("CollisionDetected", "owner.opponent", collision_offsets))
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

    possiblevels = list(range(1, penguinspec.pngvel + 1))
    if penguinspec.movevel > penguinspec.pngvel:
        possiblevels.append(penguinspec.movevel)

    ##definitions.append(ExpressionDefinitionBuilder("d_pushing_index_max", ExpressionBuilder(15).build()))
    ##definitions.append(pgpushingdef(penguinspec))
    ##definitions.append(pgsbinitdef(penguinspec))
    ##definitions.append(pngdeadptsdef(islandspec, possiblevels))
    collision_ostat = collisionoffsets(penguinspec.radius, penguinspec.movevel, penguinspec.radius, penguinspec.movevel)
    collision_opng = collisionoffsets(penguinspec.radius, penguinspec.pngvel, penguinspec.radius, penguinspec.pngvel)
    definitions.append(coldetecteddf("CollisionDetected", "opponent", collision_opng))
    ##definitions += pgpusheddefs(islandspec, penguinspec, possiblevels)
    definitions.append(pgconstcollisiondef("StaticCollisionInitialized", penguinspec.movevel, collision_ostat))
    definitions.append(pgconstcollisiondef("PushingCollisionInitialized", penguinspec.pngvel, collision_opng))

    return definitions


def pgpushingdef(penguinspec):
    pngmoves = movement.moves(penguinspec.pngvel)
    return movecase(pngmoves, "PushingPosChanged")


def pgpusheddefs(islandspec, penguinspec, possible_velocities):
    position_def = CaseDefinitionBuilder("PushedPosChanged")
    index_init_def = CaseDefinitionBuilder("PushedInitIndex")
    index_exp = ExpressionBuilder("pushed_index")
    velocity_exp = ExpressionBuilder("pushed_velocity")
    append = lambda exp1, exp2: exp1.withand(exp2)
    max_index = 0

    for v in possible_velocities:
        pushed_list = movement.fricvelext(penguinspec.mass, islandspec.friction, v, 1)
        max_value_exp = ExpressionBuilder(len(pushed_list) - 1)
        index_init_def = index_init_def.withcase(velocity_exp.withnext().witheq(ExpressionBuilder(v)).build(), max_value_exp.build())

        if len(pushed_list) > max_index:
            max_index = len(pushed_list) - 1

        for index in range(1, len(pushed_list)):
            pushed_moves = movement.moves(pushed_list[index])
            temp_case = movecase(pushed_moves, position_def.name())
            temp_case = temp_case.withexpappended(index_exp.witheq(ExpressionBuilder(index)), append)
            temp_case = temp_case.withexpappended(velocity_exp.witheq(ExpressionBuilder(v)), append)
            position_def = position_def.combined(temp_case)

    index_init_def = index_init_def.withcase(ExpressionBuilder.true().build(), ExpressionBuilder(0).build())
    position_def = position_def.withcase(ExpressionBuilder.true().build(), ExpressionBuilder.false().build())
    max_index_def = ExpressionDefinitionBuilder("d_penguin_pushed_index_max").withexp(ExpressionBuilder(max_index).build())

    return [max_index_def, index_init_def, position_def]


def pgconstcollisiondef(name, velocity, collision_offsets):
    collision_def = CaseDefinitionBuilder(name)
    ox_exp = ExpressionBuilder("opponent.x - x").withparen()
    oy_exp = ExpressionBuilder("opponent.y - y").withparen()
    ndir_exp = ExpressionBuilder("direction").withnext()
    nvel_exp = ExpressionBuilder("pushed_velocity").withnext().witheq(ExpressionBuilder(velocity))

    for x, yList in collision_offsets.items():
        tx_exp = ox_exp.witheq(ExpressionBuilder(x))
        for y in yList:
            ty_exp = oy_exp.witheq(ExpressionBuilder(y))
            if x == 0:
                if y > 0:
                    next_direction = 270
                else:
                    next_direction = 90
            elif x > 0 and y >= 0:
                next_direction = 180 + round(math.atan(y/x) * 180/math.pi)
            elif x > 0 and y < 0:
                next_direction = 180 - round(math.atan(-y/x) * 180 / math.pi)
            elif x < 0 and y > 0:
                next_direction = 359 - round(math.atan(y/-x) * 180 / math.pi)
            elif x < 0 and y <= 0:
                next_direction = round(math.atan(-y/-x) * 180 / math.pi)

            case_exp = tx_exp.withand(ty_exp).withand(ndir_exp.witheq(ExpressionBuilder(next_direction)))
            case_exp = case_exp.withand(nvel_exp)

            collision_def = collision_def.withcase(case_exp.build(), ExpressionBuilder.true().build())

    collision_def = collision_def.withcase(ExpressionBuilder.true().build(), ExpressionBuilder.false().build())
    return collision_def

'''
def pgconstcollisiondef(name, velocity, collision_offsets):
    collision_def = CaseDefinitionBuilder(name)
    ox_exp = ExpressionBuilder("opponent.x - x").withparen()
    oy_exp = ExpressionBuilder("opponent.y - y").withparen()
    ndir_exp = ExpressionBuilder("direction").withnext()
    nvel_exp = ExpressionBuilder("pushed_velocity").withnext().witheq(ExpressionBuilder(velocity))
    ox_restr_exp = ox_exp.withge(ExpressionBuilder(-54)).withand(ox_exp.withle(ExpressionBuilder(54)))
    oy_restr_exp = oy_exp.withge(ExpressionBuilder(-54)).withand(oy_exp.withle(ExpressionBuilder(54)))

    xx_exp = ox_exp.withmul(ox_exp)
    yy_exp = oy_exp.withmul(oy_exp)
    xy_exp = ox_exp.withmul(oy_exp)
    yycoef_exp = yy_exp.withmul(ExpressionBuilder(28125)).withparen().withdiv(ExpressionBuilder(100000))
    atan_top = ExpressionBuilder(18000).withmul(xy_exp).withparen()
    atan_bottom = ExpressionBuilder(314).withmul(xx_exp.withadd(yycoef_exp)).withparen()
    atan_exp = atan_top.withdiv(atan_bottom).withparen()

    # x = 0 and y > 0
    temp_exp = ox_exp.witheq(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withgt(ExpressionBuilder(0)))
    temp_exp = temp_exp.withand(ndir_exp.witheq(ExpressionBuilder(90)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x = 0 and y < 0
    temp_exp = ox_exp.witheq(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withlt(ExpressionBuilder(0)))
    temp_exp = temp_exp.withand(ndir_exp.witheq(ExpressionBuilder(270)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x > 0 and y >= 0 y <= x 1-oct
    temp_exp = ox_exp.withgt(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withge(ExpressionBuilder(0)))
    temp_exp = temp_exp.withand(oy_exp.withle(ox_exp))
    temp_exp = temp_exp.withnewline().withand(ndir_exp.witheq(atan_exp))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x > 0 and y > x 2 or 3 oct
    temp_exp = oy_exp.withgt(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withgt(ox_exp))
    temp_exp = temp_exp.withnewline().withand(ndir_exp.witheq(ExpressionBuilder(90).withsub(atan_exp)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x < 0 and y > -x
    temp_exp = ox_exp.withlt(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withadd(ox_exp).withgt(ExpressionBuilder(0)))
    temp_exp = temp_exp.withnewline().withand(ndir_exp.witheq(ExpressionBuilder(90).withsub(atan_exp)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x < 0 and y >= 0 and y <= -x
    temp_exp = ox_exp.withlt(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withge(ExpressionBuilder(0)))
    temp_exp = temp_exp.withand(oy_exp.withadd(ox_exp).withle(ExpressionBuilder(0)))
    temp_exp = temp_exp.withnewline().withand(ndir_exp.witheq(ExpressionBuilder(180).withadd(atan_exp)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x < 0 and y < 0 and y >= x
    temp_exp = ox_exp.withlt(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withlt(ExpressionBuilder(0)))
    temp_exp = temp_exp.withand(oy_exp.withge(ox_exp))
    temp_exp = temp_exp.withnewline().withand(ndir_exp.witheq(ExpressionBuilder(180).withadd(atan_exp)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x < 0 and y < 0 and y < x
    temp_exp = ox_exp.withlt(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withlt(ExpressionBuilder(0)))
    temp_exp = temp_exp.withand(oy_exp.withlt(ox_exp))
    temp_exp = temp_exp.withnewline().withand(ndir_exp.witheq(ExpressionBuilder(270).withsub(atan_exp)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x > 0 and y < 0 and y + x < 0
    temp_exp = ox_exp.withlt(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withlt(ExpressionBuilder(0)))
    temp_exp = temp_exp.withand(oy_exp.withadd(ox_exp).withlt(ExpressionBuilder(0)))
    temp_exp = temp_exp.withnewline().withand(ndir_exp.witheq(ExpressionBuilder(270).withsub(atan_exp)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    # x > 0 and y < 0 and y + x >= 0
    temp_exp = ox_exp.withlt(ExpressionBuilder(0))
    temp_exp = temp_exp.withand(oy_exp.withlt(ExpressionBuilder(0)))
    temp_exp = temp_exp.withand(oy_exp.withadd(ox_exp).withge(ExpressionBuilder(0)))
    temp_exp = temp_exp.withnewline().withand(ndir_exp.witheq(ExpressionBuilder(359).withadd(atan_exp)))
    collision_def = collision_def.withcase(temp_exp.build(), ExpressionBuilder.true().build())

    append = lambda exp1, exp2: exp1.withand(exp2)
    collision_def = collision_def.withexpappended(nvel_exp, append)
    collision_def = collision_def.withexpappended(ox_restr_exp, append)
    collision_def = collision_def.withexpappended(oy_restr_exp, append)

    collision_def = collision_def.withcase(ExpressionBuilder.true().build(), ExpressionBuilder.false().build())

    return collision_def'''

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


def coldetecteddf(name, path, offsets):
    casedef = CaseDefinitionBuilder(name)
    xexp = ExpressionBuilder("x").withnext()
    yexp = ExpressionBuilder("y").withnext()

    pxexp = ExpressionBuilder(path + ".x").withnext()
    pyexp = ExpressionBuilder(path + ".y").withnext()

    nexpx = pxexp.withsub(xexp).withparen()
    nexpy = pyexp.withsub(yexp).withparen()

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
                expression = direxp.withnext().within(ExpressionBuilder(direction, i-1))
            else:
                expression = direxp.withnext().witheq(ExpressionBuilder(direction))

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


def collisionoffsets(srcrad, srcvel, destrad, destvel):
    colradius = srcrad + destrad
    veloffset = srcvel + destvel
    smallradius = colradius - veloffset

    offsets = {}
    for x in range(-colradius, colradius + 1):
        for y in range(-colradius, colradius + 1):
            if (x * x + y * y >= smallradius*smallradius) and (x * x + y * y <= colradius * colradius):
                if x not in offsets:
                    offsets[x] = []
                offsets[x].append(y)

    return offsets
