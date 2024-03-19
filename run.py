from Bisection_method import OneMaxReport, TrapKReport, LeadingOneReport
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--benchmark', type=str)
parser.add_argument('--save_file_path', type=str)
args = parser.parse_args()

def main():
    if args.benchmark == 'onemax':
        OneMaxReport(f'{args.save_file_path}', '1X')
        OneMaxReport(f'{args.save_file_path}', 'UX')
    elif args.benchmark == 'leadingone':
        LeadingOneReport(f'{args.save_file_path}', '1X')
        LeadingOneReport(f'{args.save_file_path}', 'UX')
    elif args.benchmark == 'concatenated_trap_k':
        TrapKReport(f'{args.save_file_path}', '1X')
        TrapKReport(f'{args.save_file_path}', 'UX')
    return

if __name__ == '__main__':
    main()
