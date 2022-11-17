import csv

class CSVExporter:
    @classmethod
    def export(cls, filename, log):
        with open(filename, 'w') as csvfile:
            fieldnames = ['algorithm', 'trial', 'function', 'population', 'crossover_probability', 'mutation_probability', 'best_solution', 'value', 'recombination', 'c1', 'c2', 'w']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in log:
                writer.writerow(row)

