* This file has a strange (new) constraint name in the RANGES data section. That
* is not the place where new constraints can be introduced, and likely points
* to a data issue the implementation should warn about.
NAME          UnknownConstraintRanges
ROWS
 N  OBJ
 E  CONSTR
COLUMNS
    X1        OBJ       10.0
    X1        CONSTR    5
RHS
    RHS       CONSTR    8.0
RANGES
* "STRANGE" is a new, unknown constraint.
    RHS       STRANGE    5.0
ENDATA
