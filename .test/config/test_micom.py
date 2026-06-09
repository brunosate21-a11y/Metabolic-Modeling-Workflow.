from micom.data import test_taxonomy
from micom import Community

tax = test_taxonomy()
com = Community(tax)
sol = com.cooperative_tradeoff()
print(sol.members)