"""Exact algebra supplements the analytic proof; it is not a tensor test."""
from fractions import Fraction as Q
from itertools import product
import unittest
import sympy as s


def cube(a,b):
    u,v=sorted((Q(a),Q(b)))
    return (3*u-1)/2*(v+(u-1)/2)**3


class ProfileProofTests(unittest.TestCase):
    def test_symbolic_derivatives_and_join(self):
        x,A=s.symbols('x A',positive=True)
        f=(x/2)**s.Rational(1,3)*(2*A+x)/6
        second=2**s.Rational(2,3)*(x-A)/(3*x**s.Rational(5,3))
        self.assertEqual(s.simplify(9*s.diff(f,x,2)-second),0)
        self.assertEqual(s.simplify(3*s.diff(f,x).subs(x,A)-(A/2)**s.Rational(1,3)),0)
        # This expression has positive coefficients when x,A>0.
        self.assertEqual(s.simplify(3*s.diff(f,x)-(A+2*x)/(3*2**s.Rational(1,3)*x**s.Rational(2,3))),0)

    def test_boundary_envelope_and_tripling(self):
        for a in range(1,101):
            self.assertEqual(cube(1,a),a**3)
            self.assertEqual(cube(a,a),Q(3*a-1,2)**4)
            for h in range(1,101):
                self.assertGreaterEqual(cube(a,3*h+a-1),27*cube(a,h))
                self.assertLessEqual(cube(a,h),Q(a+h-1)**4)

    def test_symbolic_linear_extension(self):
        A,H=s.symbols('A H')
        self.assertEqual(s.expand(A*(A+2*H)**3-H*(2*A+H)**3-(A-H)**3*(A+H)),0)
        for a in range(1,41):
            for h in range(1,41):
                d=Q(a-1,2)
                self.assertLessEqual(cube(a,h),Q(3*a-1,2)*(h+d)**3)

    def test_sector_dimensions_and_sufficient_bound(self):
        for blocks in range(2,51):
            self.assertEqual(min(max(r,blocks-r-1) for r in range(blocks+1)),blocks//2)
        # Test the rational linear upper bound on each summand, avoiding
        # floating-point cube roots of sums of radicals.
        for a in range(1,9):
            d=Q(a-1,2)
            for blocks in range(2,6):
                for lengths in product(sorted({1,a,max(1,a-1),2*a}),repeat=blocks):
                    B=sum(lengths)+(blocks//2)*(a-1)
                    self.assertGreaterEqual(B,a)
                    self.assertGreaterEqual(B+d,sum(Q(h)+d for h in lengths))

    def test_false_unshifted_tripling_rejected(self):
        # Omitting the additive a-1 shift is not justified; a concrete
        # counterexample guards against silently extending the claim.
        self.assertLess(cube(2,3*2),27*cube(2,2))


if __name__=='__main__':unittest.main()
