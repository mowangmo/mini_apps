# def foo(x, y, *args, a=1, b, **kwargs):
#     print(x, y)
#     print(args)
#     print(a)
#     print(b)
#     print(kwargs)
#
#
# foo(1, 2, 3, 4, 5, b=3, c=4, d=5)

def foo(args):
    print(args[0])

foo([1,23])