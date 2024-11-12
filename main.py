import json
import time
from Chomsky import GrammarCNFTransformer
from CYK import CYKGrammarParser

def main():
    # Load context-free grammar from a JSON file
    with open("input.json", "r") as grammar_file:
        grammar = json.load(grammar_file)

    # Initialize the CNF transformer
    cnf_converter = GrammarCNFTransformer(grammar)
    
    # Convert the CFG to CNF
    cnf_grammar = cnf_converter.convert_to_cnf()
    print("Converted CNF Grammar:")
    print(json.dumps(cnf_grammar, indent=4))

    # Optionally save the converted CNF grammar to a file
    with open("cnf_grammar.json", "w") as cnf_file:
        json.dump(cnf_grammar, cnf_file, indent=4)

    # Start CYK Parsing
    sentence = input("Please enter a sentence to parse: ")
    start_time = time.time()
    cyk_parser = CYKGrammarParser(cnf_grammar)
    is_accepted = cyk_parser.parse(sentence)
    
    # Output the result
    if is_accepted:
        print(f"The sentence '{sentence}' is in the language.")
        print("CYK Table:")
        cyk_parser.print_table()
        cyk_parser.generate_parse_tree_graph(output_file="parse_tree")
    else:
        print(f"The sentence '{sentence}' is not in the language.")

    # Display parsing time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parsing completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
