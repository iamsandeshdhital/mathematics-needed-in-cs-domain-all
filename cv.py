import io, re
root = io.open("README.md", encoding="utf-8").read()
canon = set(re.findall(r"\]\((part\d\d_[a-z_]+/\d\d_[a-z0-9_]+\.md)\)", root))
targets = [
 "part01_logic_proof/15_sets_and_cardinality.md",
 "part01_logic_proof/14_mathematical_induction.md",
 "part02_discrete_combinatorics/20_counting_principles.md",
 "part02_discrete_combinatorics/21_permutations_and_combinations.md",
 "part02_discrete_combinatorics/23_inclusion_exclusion_and_pigeonhole.md",
 "part02_discrete_combinatorics/24_recurrence_relations.md",
 "part02_discrete_combinatorics/25_relations_and_equivalence_classes.md",
 "part02_discrete_combinatorics/28_counting_strategies.md",
 "part03_linear_algebra/38_orthogonality_and_least_squares.md",
 "part03_linear_algebra/40_svd_and_pca.md",
 "part04_calculus/52_integration.md",
 "part04_calculus/55_fourier_series_and_transforms.md",
 "part06_algorithms_math/80_big_o_and_complexity.md",
]
for t in targets:
    print(("OK  " if t in canon else "MISMATCH ") + t)
