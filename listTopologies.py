# Consider the discrete topology on X
# X_Discrete = { {} {a} {b} {c} {a,b} {a,c} {b,c} {a,b,c} }

# Let the set Y contain all nontrivial elements of X_discrete
# Y = { {a} {b} {c} {a,b} {a,c} {b,c} }

# Notice that for any subset Z of Y, the following union is a basis for some topology
#    Z \union {} \union {a,b,c}

# There are 2^6=64 such generating sets, but several of them may generate the same topology
# For example, both of the bases below generate X_Discrete (once {} and X are included)
#     Z_111000 = Z_56 = { {a}, {b}, {c} }
#     Z_111111 = Z_63 = { {a}, {b}, {c}, {ab}, {ac}, {bc} }

# Let the relation ~ indicate that two sets Z_i and Z_j are equivalent if Z_i and Z_j 
# generate the same topology.  
#
# '~' is an equivalence relation for all the same reasons that '=' is.

# This program generates a topology for each of these bases, so the number (and size) of 
# the resultant equivalence classes can be explored

NullSet_str = "{} "
A_str =  "{a} "
B_str =  "{b} "
C_str =  "{c} "
AB_str = "{a,b} "
AC_str = "{a,c} "
BC_str = "{b,c} "
ABC_str = "{a,b,c} "

nullSet = 0b10000000
a =       0b01000000
b =       0b00100000
c =       0b00010000
ab =      0b00001000
ac =      0b00000100
bc =      0b00000010
abc =     0b00000001

# The only unions we must compute are those resulting in {a,b}, {a,c}, and {b,c}

def TryUnionAB(gen):
    if ((gen & a != 0) & (gen & b != 0)):   # if both {a} and {b} are present
        return gen | ab                     # include {a,b}
    else:                                   # else
        return gen                          # make no change

def TryUnionAC(gen):
    if ((gen & a != 0) & (gen & c != 0)):
        return gen | ac
    else:
        return gen

def TryUnionBC(gen):
    if ((gen & b != 0) & (gen & c != 0)):
        return gen | bc
    else:
        return gen

# The only intersections we must compute are those resulting in {a} {b} or {c}

def TryIntersectA(gen):     
    if ((gen & ab != 0) & (gen & ac != 0)): # if both {ab} and {ac} are present
        return gen | a                      # include {a}
    else:                                   # else
        return gen                          # make no change

def TryIntersectB(gen):
    if ((gen & ab != 0) & (gen & bc != 0)):
        return gen | b
    else:
        return gen

def TryIntersectC(gen):
    if ((gen & ac != 0) & (gen & bc != 0)):
        return gen | c
    else:
        return gen
    

def GenerateTopology(Z):
    protoTopo = (Z << 1) | nullSet | abc    # shift so Z's sets line up with X_discrete's nontrivial sets

    previous = 0

    while protoTopo != previous:            # Keep generating the topology until no more changes can be made
        previous = protoTopo
        protoTopo = TryUnionAB(protoTopo)
        protoTopo = TryUnionAC(protoTopo)
        protoTopo = TryUnionBC(protoTopo)
        protoTopo = TryIntersectA(protoTopo)
        protoTopo = TryIntersectB(protoTopo)
        protoTopo = TryIntersectC(protoTopo)

    return protoTopo

TopologiesOnX = set();
for Z in range(0,64):
    Topo = GenerateTopology(Z)
    TopologiesOnX.add(Topo)
    print "Z_{0:{fill}6b} generates topology: {1:b} ({2:d})".format(Z,Topo,Topo,fill='0')

n = 1
print "\nTopologies on X:\n"
for T in TopologiesOnX:
    print'{0: <2}'.format("%d" %n),
    print "(%d):" %T,
    print "{ ",
    if ((T & nullSet) != 0):
        print NullSet_str,

    if ((T & a) != 0):
        print A_str,
    else:
        print "    ",

    if ((T & b) != 0):
        print B_str,
    else:
        print "    ",

    if ((T & c) != 0):
        print C_str,
    else:
        print "    ",

    if ((T & ab) != 0):
        print AB_str,
    else:
        print "      ",

    if ((T & ac) != 0):
        print AC_str,
    else:
        print "      ",

    if ((T & bc) != 0):
        print BC_str,
    else:
        print "      ",

    if ((T & abc) != 0):
        print ABC_str,

    print "}"
    n += 1




