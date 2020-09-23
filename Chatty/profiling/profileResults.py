import pstats

p = pstats.Stats('stats.prof')
while True:
    p.sort_stats(input("Metric: ")).print_stats(10)
