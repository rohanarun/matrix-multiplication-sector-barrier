"""Exact algebra supplements the analytic proof; it is not a tensor test."""
from fractions import Fraction as Q
from itertools import product
import unittest
import sympy as s


def cube(a,b):
    u,v=sorted((Q(a),Q(b)))
    return (3*u-1)/2*(v+(u-1)/2)**3


H_CACHE={1:Q(1)}
def H(u):
    # H_u = prod_{m<u} (1+1/(3m)), the source's normalized-growth product.
    while max(H_CACHE)<u:
        m=max(H_CACHE)
        H_CACHE[m+1]=H_CACHE[m]*(1+Q(1,3*m))
    return H_CACHE[u]


def least(a,b):
    u,v=sorted((a,b))
    return H(u)*(Q(v)+Q(u-1,2))


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

    def test_exact_sector_saturation_and_parity(self):
        # In this family all radicals share the positive factor L, so
        # cubing compares the actual equality exactly with rational numbers.
        for a in range(1,20):
            d=Q(a-1,2)
            Lcube=Q(3*a-1,2)
            for blocks in range(2,16):
                lengths=[a+i for i in range(blocks)]
                B=sum(lengths)+(blocks//2)*(a-1)
                sum_coefficient=sum(Q(h)+d for h in lengths)
                gap_coefficient=Q(B)+d-sum_coefficient
                expected=0 if blocks%2 else d
                self.assertEqual(gap_coefficient,expected)
                self.assertEqual(cube(a,B),Lcube*(sum_coefficient+expected)**3)
                if blocks%2 or a==1:
                    self.assertEqual(cube(a,B),Lcube*sum_coefficient**3)
                else:
                    self.assertGreater(cube(a,B),Lcube*sum_coefficient**3)
                self.assertGreater(cube(a,B+1),cube(a,B))

    def test_short_sector_deficit_is_strict(self):
        for a in range(2,30):
            for h in range(1,a):
                d=Q(a-1,2)
                self.assertLess(cube(a,h),Q(3*a-1,2)*(h+d)**3)


class LeastProfileTests(unittest.TestCase):
    N=80

    def test_growth_product_is_gamma_ratio(self):
        third=s.Rational(1,3)
        for a in range(1,41):
            exact=s.gamma(a+third)/(s.gamma(a)*s.gamma(1+third))
            self.assertEqual(s.gammasimp(exact),s.Rational(H(a).numerator,H(a).denominator))
            self.assertEqual(s.rf(s.Rational(4,3),a-1)/s.factorial(a-1),s.Rational(H(a).numerator,H(a).denominator))

    def test_least_profile_is_admissible_exactly(self):
        N=self.N
        for a in range(1,N+1):
            self.assertEqual(least(1,a),a)
            self.assertEqual(least(a,a),Q(3*a-1,2)*H(a))
            for b in range(2,N):
                self.assertGreaterEqual(2*least(a,b),least(a,b+1)+least(a,b-1))
            for h in range(1,N+1):
                lhs,rhs=least(a,3*h+a-1),3*least(a,h)
                self.assertGreaterEqual(lhs,rhs)
                # Equality in shifted tripling holds exactly when h >= a-1.
                self.assertEqual(lhs==rhs,h>=a-1)
                # Rank envelope at t=3/4, compared by cubing (no radicals).
                self.assertLessEqual(least(a,h)**3,Q(a+h-1)**4)

    def test_ratio_lemma_and_induction_identities(self):
        for h in range(1,41):
            for a in range(h,61):
                g=H(a)*(a+2*h-1)-H(h)*(2*a+h-1)
                self.assertGreaterEqual(g,0)
                self.assertEqual(g==0,a<=h+1)
        a,h,b,m,Hb=s.symbols('a h b m H_b',positive=True)
        self.assertEqual(s.expand((2*a+h-1)*(4*a+2*h)-6*a*(a+2*h-1)-2*(a-h)*(a-h+1)),0)
        H1=Hb*(3*b+1)/(3*b); H2=H1*(3*b+4)/(3*b+3)
        self.assertEqual(s.simplify(2*H1-Hb-H2-2*Hb/(9*b*(b+1))),0)
        self.assertEqual(s.expand((3*m+2)*27*m**3-(3*m+1)**3*(3*m-1)-(6*m+1)),0)

    def test_least_profile_below_star_with_increasing_ratio(self):
        # P_* / P_min = ((3u-1)/2)^{1/3} / H_u; compare cubes exactly.
        prev=Q(1)
        for u in range(1,200):
            ratio_cubed=Q(3*u-1,2)/H(u)**3
            self.assertGreaterEqual(ratio_cubed,1)
            self.assertEqual(ratio_cubed==1,u==1)
            self.assertGreaterEqual(ratio_cubed,prev)
            self.assertLess(ratio_cubed,Q(10223,10000)**3)
            prev=ratio_cubed
        for a in range(1,40):
            for b in range(1,40):
                self.assertLessEqual(least(a,b)**3,cube(a,b))

    def test_minimality_chain_on_star_profile(self):
        # The proof of minimality bounds every admissible P from below by
        # H^P_a (b+(a-1)/2) with H^P_a = 2P(a,a)/(3a-1); check the chain on
        # P_* (cubes keep everything rational) and the recursion on P_min.
        for a in range(1,40):
            HP_cubed=Q(2,3*a-1)**3*cube(a,a)
            self.assertGreaterEqual(HP_cubed,H(a)**3)
            for b in range(a,60):
                self.assertGreaterEqual(cube(a,b),HP_cubed*(b+Q(a-1,2))**3)
        for a in range(2,200):
            self.assertEqual(H(a),(1+Q(1,3*(a-1)))*H(a-1))
            self.assertGreaterEqual(H(a)**3,a)  # the source's a^{4/3} bound

    def test_growth_constant_limit(self):
        limit=s.Rational(3,2)/s.gamma(s.Rational(4,3))
        for a in (10**3,10**4):
            value=s.Rational(3*a-1,2)*s.gamma(a+s.Rational(1,3))/(s.gamma(a)*s.gamma(s.Rational(4,3)))/s.Integer(a)**s.Rational(4,3)
            self.assertLess(abs(s.N(value-limit,30)),s.Rational(1,a))
        self.assertLess(abs(s.N(limit-s.Rational(167977,100000),20)),s.Rational(1,100000))

    def test_least_profile_sector_saturation(self):
        for a in range(1,16):
            d=Q(a-1,2)
            for blocks in range(2,10):
                for shift in (-1,0,1):
                    lengths=[max(1,a+shift+i) for i in range(blocks)]
                    B=sum(lengths)+(blocks//2)*(a-1)
                    gap=least(a,B)-sum(least(a,h) for h in lengths)
                    self.assertGreaterEqual(gap,0)
                    parity=0 if blocks%2 else H(a)*d
                    deficit=sum(H(a)*(h+d)-least(a,h) for h in lengths)
                    self.assertEqual(gap,parity+deficit)
                    self.assertEqual(deficit==0,all(h>=a-1 for h in lengths))


if __name__=='__main__':unittest.main()
