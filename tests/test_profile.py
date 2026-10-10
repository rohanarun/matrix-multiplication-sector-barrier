"""Exact algebra supplements the analytic proof; it is not a tensor test."""
from fractions import Fraction as Q
from itertools import permutations, product
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


LEGS=('X','Y','Z')
PLACEMENTS=[p for p in permutations(LEGS)]


def swap12(pi):return (pi[1],pi[0],pi[2])
def swap23(pi):return (pi[0],pi[2],pi[1])


def flattening(F):
    # Values of the flattening character along lambda-leg F on C(a,b)^pi,
    # and its dot-product exponents.
    exps={L:(0 if L==F else 1) for L in LEGS}
    def ell(pi,a,b):return (a,b,a+b-1)[pi.index(F)]
    return ell,exps


class LegResolvedTests(unittest.TestCase):
    N=24

    def test_hoelder_form_stationarity_and_value(self):
        p=s.symbols('p',positive=True)
        A=s.symbols('A1:4',positive=True)
        S_=sum(Ai**(1/p) for Ai in A)
        q=[Ai**(1/p)/S_ for Ai in A]
        grads=[s.log(Ai)-p*s.log(qi)-p for Ai,qi in zip(A,q)]
        for g in grads[1:]:
            self.assertEqual(s.simplify(s.expand_log(g-grads[0],force=True)),0)
        value=sum(qi*(s.log(Ai)-p*s.log(qi)) for Ai,qi in zip(A,q))
        self.assertEqual(s.simplify(s.expand_log(value-p*s.log(S_),force=True)),0)
        # Rational probe: the entropy form never exceeds the Hoelder form.
        import math
        for vals,pp in (((3,5,2),Q(3,4)),((1,1,4),Q(1,2)),((2,7,7),1)):
            target=sum(v**(1/float(pp)) for v in vals)**float(pp)
            best=0
            for i in range(1,20):
                for j in range(1,20-i):
                    qv=(i/20,j/20,(20-i-j)/20)
                    ent=-sum(x*math.log(x) for x in qv if x>0)
                    best=max(best,math.exp(float(pp)*ent)*math.prod(v**x for v,x in zip(vals,qv)))
            self.assertLessEqual(best,target*(1+1e-12))

    def test_flattening_characters_are_leg_resolved_solutions(self):
        N=self.N
        for F in LEGS:
            ell,exps=flattening(F)
            for pi in PLACEMENTS:
                p=exps[pi[0]]
                for a in range(1,N+1):
                    for b in range(1,N+1):
                        v=ell(pi,a,b)
                        self.assertEqual(ell(pi,1,b),b**exps[pi[0]])
                        self.assertEqual(ell(pi,a,1),a**exps[pi[1]])
                        self.assertEqual(ell(pi,b,a),ell(swap12(pi),a,b))
                        self.assertTrue(1<=v<=a+b-1)
                        self.assertLessEqual(v,ell(pi,a+1,b))
                        self.assertLessEqual(v,ell(pi,a,b+1))
                        if b>=2:
                            if p==1:
                                self.assertEqual(2*v,ell(pi,a,b+1)+ell(pi,a,b-1))
                            else:
                                self.assertGreaterEqual(v,max(ell(pi,a,b+1),ell(pi,a,b-1)))
                        h=b
                        lhs=ell(pi,a,3*h+a-1)
                        parts=(ell(pi,a,h),ell(pi,a,h),ell(swap23(pi),a,h))
                        if p==1:
                            self.assertEqual(lhs,sum(parts))
                        else:
                            self.assertGreaterEqual(lhs,max(parts))

    def test_symmetric_least_assignment_is_leg_resolved_solution(self):
        # ell = P_min^{3/4}, p = 3/4: raise each Hoelder inequality to 4/3 and
        # compare rationals. Sector inequalities use the packing bound.
        N=self.N
        for a in range(1,N+1):
            self.assertEqual(least(a,1),a)
            for b in range(2,N+1):
                self.assertGreaterEqual(2*least(a,b),least(a,b+1)+least(a,b-1))
            for h in range(1,N+1):
                self.assertGreaterEqual(least(a,3*h+a-1),3*least(a,h))
                self.assertLessEqual(least(a,h)**3,Q(a+h-1)**4)
            for blocks in range(2,6):
                for lengths in product((1,max(1,a-1),a,a+2),repeat=blocks):
                    B=sum(lengths)+(blocks//2)*(a-1)
                    self.assertGreaterEqual(least(a,B),sum(least(a,h) for h in lengths))

    def test_log_mixture_is_a_solution(self):
        # Convexity in (log ell, p): the geometric mean of the symmetric
        # assignment and the output flattening, with averaged exponents.
        from mpmath import mp,mpf,power
        mp.dps=40
        tol=mpf('1e-30')
        ellZ,expZ=flattening('Z')
        exps={L:(mpf(3)/4+expZ[L])/2 for L in LEGS}
        def ell(pi,a,b):
            v=least(a,b)
            return power(power(mpf(v.numerator)/v.denominator,mpf(3)/4)*ellZ(pi,a,b),mpf(1)/2)
        def phi(p,vals):return power(sum(power(v,1/p) for v in vals),p)
        N=12
        for pi in PLACEMENTS:
            p=exps[pi[0]]
            for a in range(1,N+1):
                for b in range(1,N+1):
                    v=ell(pi,a,b)
                    self.assertLess(abs(ell(pi,1,b)-power(b,exps[pi[0]])),tol)
                    self.assertLess(abs(ell(pi,a,1)-power(a,exps[pi[1]])),tol)
                    self.assertLess(abs(v-ell(swap12(pi),b,a)),tol)
                    self.assertLessEqual(v,a+b-1+tol)
                    if b>=2:
                        self.assertGreaterEqual(power(2,p)*v,phi(p,[ell(pi,a,b+1),ell(pi,a,b-1)])-tol)
                    h=b
                    self.assertGreaterEqual(ell(pi,a,3*h+a-1),phi(p,[ell(pi,a,h),ell(pi,a,h),ell(swap23(pi),a,h)])-tol)

    def test_exponent_corollary(self):
        # With p_X = p_Y = 1 the h = 1 tripling forces a^{p_Z} <= 1 for all a.
        from mpmath import mp,mpf,power
        mp.dps=30
        for pz in (mpf(1)/4,mpf(1)/2,mpf('0.01')):
            self.assertTrue(any(2*a+1<2*a+power(a,pz) for a in range(2,50)))
        self.assertTrue(all(2*a+1>=2*a+power(a,0) for a in range(1,50)))
        # The symmetric triple passes the same family for every placement.
        p=mpf(3)/4
        for a in range(1,200):
            self.assertGreaterEqual(power(2*a+1,1/p),3*power(a,1))
