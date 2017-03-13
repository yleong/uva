#!/usr/bin/env python3
import math

DEBUG=False

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        return

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def slope(self, pt2):
        if(not abs(self.x - pt2.x)): 
            return 9999999
        myslope =  ( (pt2.y - self.y) / (pt2.x - self.x) )
        if(DEBUG): print('{} slope is {}'.format(pt2, myslope))
        return myslope

    def dist(self, pt):
        return abs(math.sqrt( (self.y-pt.y)**2 + (self.x - pt.x)**2  ))

    def angleWithXAxis(self, pt):
        xAxis = Point(self.x+1, self.y)
        return angle(xAxis, self, pt)
    
def process(pts):
    if(DEBUG): print('processing')
    for pt in pts:
        if(DEBUG): print(str(pt))
    if(DEBUG): print('done processing')
    hull = graham(pts)
    if len(hull) != 4:
        return 'Ordinary Quadrilateral'
    else:
        p1 = hull[0]
        p2 = hull[1]
        p3 = hull[2]
        p4 = hull[3]

        d12 = p1.dist(p2)
        d23 = p2.dist(p3)
        d34 = p3.dist(p4)
        d41 = p4.dist(p1)

        a123 = angle(p1, p2, p3)
        a234 = angle(p2, p3, p4)
        a341 = angle(p3, p4, p1)
        a412 = angle(p4, p1, p2)

        if(DEBUG): print('sides: {} {} {} {}'.format(d12, d23, d34, d41))
        if(DEBUG): print('angles: {} {} {} {}'.format(a123, a234, a341, a412))

        rangle = math.pi / 2.0;
        if(DEBUG): print('using rangle {}'.format(rangle))
        if(DEBUG): print('equals or not? {}'.format(fequals(rangle, a123)))
        if fequals(d12, d23) and fequals(d23, d34) and fequals(d34, d41) and fequals(a123, rangle) and fequals(a234, rangle) and fequals(a341, rangle) and fequals(a412, rangle):
            return 'Square'
        elif fequals(a123, rangle) and fequals(a234, rangle) and fequals(a341, rangle) and fequals(a412, rangle) and fequals(d12, d34) and fequals(d23, d41):
            return 'Rectangle'
        elif fequals(d12, d23) and fequals(d23, d34) and fequals(d34, d41) and not fequals(a123, rangle) and not fequals(a234, rangle) and not fequals(a341, rangle) and not fequals(a412, rangle):
            return 'Rhombus'
        elif fequals(d12, d34) and fequals(d23, d41) and not fequals(a123, rangle) and not fequals(a234, rangle) and not fequals(a341, rangle) and not fequals(a412, rangle):
            return 'Parallelogram'
        elif not intersect(p1, p2, p3, p4) or not intersect(p2, p3, p1, p4):
            return 'Trapezium'
        else:
            return 'Ordinary Quadrilateral'


# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def fequals(f1, f2):
    threshold = 1e-5
    return abs(f1-f2) < threshold

def angle(p1, p2, p3):
    """ get angle p1p2p3 """
    a = p1.dist(p2)
    b = p3.dist(p2)
    c = p1.dist(p3)
    return math.acos((a**2 + b**2 - c**2 ) / (2 * a * b))

def graham(pts):
    # first, pick the lower left hand corner
    lowest = Point(10000, 10000) #upper limit as specified in question
    for pt in pts:
        if pt.y < lowest.y:
            lowest = pt
        elif pt.y == lowest.y and pt.x < lowest.x:
            lowest = pt
        
    if(DEBUG): print('got lowest as {}'.format(lowest))
    pts.remove(lowest)
    if(DEBUG): print('before sort array is {}'.format(pts))
    # then, sort the points according to angle
    pts = sorted(pts, key=lowest.angleWithXAxis)

    if(DEBUG): print('sorted array is {}'.format(pts))

    hull = []
    hull.append(lowest)
    hull.append(pts[0])
    pts.remove(pts[0])

    while len(pts) > 0:
        currpt = hull[len(hull)-1]
        prevpt = hull[len(hull)-2]
        newpt = pts[0]
        if ccw(prevpt, currpt, newpt) >= 0:
            hull.append(newpt)
            pts.remove(newpt)
        else:
            # currpt is bad
            hull.remove(currpt)
    if(DEBUG): print('final hull is {}'.format(hull))
    return hull


# From Wikipedia
# Three points are a counter-clockwise turn if ccw > 0, clockwise if
# ccw < 0, and collinear if ccw = 0 because ccw is a determinant that
# gives twice the signed  area of the triangle formed by p1, p2 and p3.
def ccw(p1, p2, p3):
    return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)

def main():
    t = int(input())
    for i in range(0, t):
        points = []
        for j in range(0, 4):
            x, y = input().split(' ')
            points.append(Point(x, y))
        print('Case {}: {}'.format(i+1, process(points)))

if __name__ == '__main__':
    main();
