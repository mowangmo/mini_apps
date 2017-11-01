class A:
    def hahaha(self):
        print('A')

class B(A):
    def hahaha(self):
        super().hahaha()
        super(B,self).hahaha()
        A.hahaha(self)
        print('B')

a = A()
b = B()
b.hahaha()
super(B,b).hahaha()
