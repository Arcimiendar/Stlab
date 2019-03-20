class D:
    x = 2


class B(D):
    x = 1


class C(D):
    pass


class E(B, C):
    pass


class A(E):
    pass
