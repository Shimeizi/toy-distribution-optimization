from pulp import *
import sys

# 1650

n, m, t = map(int, sys.stdin.readline().strip().split())
prob = LpProblem("", LpMaximize)

fabrica_dados = []
for _ in range(n):
    fi, pi, fmax = map(int, sys.stdin.readline().strip().split())
    fabrica_dados.append((fi, pi, fmax))

pais_dados = []
for _ in range(m):
    pj, pmax, pmin = map(int, sys.stdin.readline().strip().split())
    pais_dados.append((pj, pmax, pmin))

crianca_dados = []
for _ in range(t):
    dados_crianca = list(map(int, sys.stdin.readline().strip().split()))
    crianca_dados.append(dados_crianca)

x = {}
for k in range(t):
    for f in crianca_dados[k][2:]:
        x[k, f] = LpVariable(f"x_{k}_{f}", 0, 1, LpBinary)

prob += lpSum(x[k, f] for k in range(t) for f in crianca_dados[k][2:])

for k in range(t):
    prob += lpSum(x[k, f] for f in crianca_dados[k][2:]) <= 1

for fi, pi, fmax in fabrica_dados:
    prob += lpSum(x[k, fi] for k in range(t) if fi in crianca_dados[k][2:]) <= fmax

for pj, pmax, pmin in pais_dados:
    prob += lpSum(x[k, f] for k in range(t) for f in crianca_dados[k][2:] if crianca_dados[k][1] == pj) >= pmin

for pj, pmax, _ in pais_dados:
    prob += lpSum(
        x[k, f]
        for k in range(t)
        for f in crianca_dados[k][2:]
        if any(fab[1] == pj and crianca_dados[k][1] != pj for fab in fabrica_dados if fab[0] == f)
    ) <= pmax

prob.solve(PULP_CBC_CMD(msg=0))

if LpStatus[prob.status] == "Optimal":
    print(int(value(prob.objective)))
else:
    print(-1)