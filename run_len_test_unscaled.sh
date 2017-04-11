#! /bin/bash


#python gs_data.py 100 10 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p10_k3
#python gs_data.py 100 10 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p20_k3
#python gs_data.py 100 10 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p30_k3
#python gs_data.py 100 10 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p40_k3
python gs_data.py 100 50 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p50_k3
python gs_data.py 100 60 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p60_k3
python gs_data.py 100 70 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p70_k3
python gs_data.py 100 80 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p80_k3
python gs_data.py 100 90 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p90_k3
python gs_data.py 100 100 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p100_k3
python gs_data.py 100 110 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p110_k3
python gs_data.py 100 120 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p120_k3
python gs_data.py 100 130 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p130_k3
python gs_data.py 100 140 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p140_k3
python gs_data.py 100 150 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p150_k3
python gs_data.py 100 160 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p160_k3
python gs_data.py 100 170 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p170_k3
python gs_data.py 100 180 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p180_k3
python gs_data.py 100 190 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p190_k3
python gs_data.py 100 200 tract_dependent_unscaled 3 ./simulated_data/len_test_n100_p200_k3

#python tract_tree.py ./simulated_data/len_test_n100_p10_k3 3 ./scratch_results >> len_test_output.txt
#python tract_tree.py ./simulated_data/len_test_n100_p20_k3 3 ./scratch_results >> len_test_output.txt
#python tract_tree.py ./simulated_data/len_test_n100_p30_k3 3 ./scratch_results >> len_test_output.txt
#python tract_tree.py ./simulated_data/len_test_n100_p40_k3 3 ./scratch_results >> len_test_output.txt
python tract_tree.py ./simulated_data/len_test_n100_p50_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p60_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p70_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p80_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p90_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p100_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p110_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p120_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p130_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p140_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p150_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p160_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p170_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p180_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p190_k3 3 ./scratch_results >> len_test_unscaled.txt
python tract_tree.py ./simulated_data/len_test_n100_p200_k3 3 ./scratch_results >> len_test_unscaled.txt



