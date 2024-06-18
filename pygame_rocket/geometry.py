import pygame

def line_intersection(p1: pygame.math.Vector2, p2: pygame.math.Vector2, q1: pygame.math.Vector2, q2: pygame.math.Vector2):
    """ 
    Returns the point of intersection of the lines between p1,p2 and q1,q2. 
    If lines would intersect outside the line segments, returns None.     
    """
    p1 = pygame.math.Vector2(p1)
    p2 = pygame.math.Vector2(p2)
    q1 = pygame.math.Vector2(q1)
    q2 = pygame.math.Vector2(q2)

    # Calculate the vectors for the two lines
    r = p2 - p1
    s = q2 - q1

    # If the lines are parallel, they don't intersect
    rxs = r.cross(s)
    if rxs == 0:
        return None

    # Calculate the vector between the two starting points    
    qmp = q1 - p1

    # Calculate the intersection point of the two lines
    t = qmp.cross(s) / rxs
    u = qmp.cross(r) / rxs

    # If t and u are between 0 and 1, the lines intersect
    if 0 <= t <= 1 and 0 <= u <= 1:
        return p1 + t * r
 
    return None

    
def boundary_intersection(boundary: pygame.Rect, pos: pygame.math.Vector2):
    """ Returns the point of intersection of the boundary with the line passing through the centre of mass and the position. """
    
    edges = (
        (boundary.topleft, boundary.topright),
        (boundary.topright, boundary.bottomright),
        (boundary.bottomright, boundary.bottomleft),
        (boundary.bottomleft, boundary.topleft)
    )
    
    for edge in edges:
        intersection = line_intersection(pos, boundary.center, *edge)
        if intersection:
            return intersection


