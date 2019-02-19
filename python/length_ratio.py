import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--ref', type=argparse.FileType('r'), required=True, help='reference file')
	parser.add_argument('--hyp', type=argparse.FileType('r'), required=True, help='hypothesis file')
	
	args = parser.parse_args()
	
	with args.ref as ref, args.hyp as hyp:
		lengths_ref = []  # type: List[int]
		lengths_hyp = []  # type: List[int]
		for ref_line, hyp_line in zip(ref, hyp):
			lengths_ref.append(len(ref_line))
			lengths_hyp.append(len(hyp_line))
	
	ratios = [hyp_len / ref_len for hyp_len, ref_len in zip(lengths_ref, lengths_hyp)]
	
	avg_length_ratio = sum(ratios) / len(ratios)
	min_length_ratio = min(ratios)
	max_length_ratio = max(ratios)
	
	for desc, value in zip(['Avg.', 'Min.', 'Max.'], [avg_length_ratio, min_length_ratio, max_length_ratio]):
		logger.info("{} length ratio: {}".format(desc, value))