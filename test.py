import mock


def func1():
    func2()


def func2():
    print ('func2')


def mocked_f2():
    print('mock')


@mock.patch('__main__.func2', mocked_f2)
def test1():
    func1()
    #import pdb;pdb.set_trace()


test1()
func1()