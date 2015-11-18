from charm.core.math.integer import integer, hashInt, randomPrime, isPrime, bitsize
from charm.toolbox.integergroup import IntegerGroupQ
from charm.toolbox.conversion import Conversion
import unittest

debug = False

NUM_BITS = 32

class IntegerTest(unittest.TestCase):

    def setUp(self):
        #print("Generating Sophie Germain primes p = 2q+1 on", NUM_BITS, "bits")
        while True:
            self.p = randomPrime(NUM_BITS, 1)
            self.q = (self.p - 1) / 2
            if isPrime(self.p) and isPrime(self.q):
                break
        #print("p =", self.p, "q =", self.q)

        self.group = IntegerGroupQ()
        self.group.p = self.p
        self.group.q = self.q
        self.group.r = integer(2)
        #print("group:", str(self.group))

    def testBasicViability(self):
        p = integer(64283)
        q = integer(32141)
        assert isPrime(p)
        assert isPrime(q)
        assert p == 2*q+1
        assert hashInt([ Conversion.bytes2integer('somedata') ], p, q, True) \
            != hashInt([ Conversion.bytes2integer('otherdata') ], p, q, True)

    def testHashInt(self):
        self._hashInt(True)
        self._hashInt(False)

    def _hashInt(self, modP):
        data = []
        hashes = dict()
        num = 256
        for i in range(0, num):
            data.append("dataDataDATAadksjdiqweqwiewqjekdasjdkladjaskdlajdl" + str(i))
            conv = Conversion.bytes2integer(data[i])
            #print("Converted", data[i], "(", len(data[i]), " bytes) data to",
            #      conv, "(", bitsize(conv) / 8, "bytes)")
            h = hashInt([ conv ], self.p, self.q, modP)
            hStr = Conversion.IP2OS(h)
            if hStr in hashes:
                j = hashes[hStr]
                print("Collision between hash #", i, " and #", j, ":", h)
                assert False
            else:
                hashes[hStr] = i
            #print(i, ' -> h("', data[i], '") = h(', conv, ') ->', h)

    # TODO: This testcase will fail
    #def testIsCongruent(self):
    #    x = self.group.random()
    #    assert self.group.isMember(x) == True

if __name__ == "__main__":
    unittest.main()
