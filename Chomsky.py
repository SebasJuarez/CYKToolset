import json

class GrammarCNFTransformer:
    def __init__(self, grammar_rules: dict, epsilon_marker: str = "epsilon") -> None:
        self.grammar = grammar_rules
        self.epsilon = epsilon_marker
        
    def is_variable_symbol(self, symbol) -> bool:
        return symbol in self.grammar["VARIABLES"]
    
    def is_terminal_symbol(self, symbol) -> bool:
        return symbol in self.grammar["TERMINALES"]
    
    def all_productions_are_terminals(self, variable) -> bool:
        rules = self.grammar["REGLAS"][variable]
        return all(self.is_terminal_symbol(rule) for rule in rules)
    
    def validate_production(self, from_variable: str, to_production: str) -> bool:
        var_check = self.is_variable_symbol(from_variable)
        production_check = all([self.is_variable_symbol(x) or self.is_terminal_symbol(x) or x == self.epsilon for x in to_production.split(" ")])
        return var_check and production_check
    
    def variable_has_productions(self, variable) -> bool:
        return variable in self.grammar["REGLAS"]
    
    def check_nullable(self, variable: str) -> bool:
        if not self.variable_has_productions(variable) or variable == self.grammar["INICIAL"]:
            return False
        productions = self.grammar["REGLAS"][variable]

        if any([production == self.epsilon for production in productions]):
            return True

        for production in productions:
            if all(self.is_variable_symbol(sym) for sym in production.split(" ")):
                if any(self.all_productions_are_terminals(var) or var != variable for var in production.split(" ")):
                    return False
                nullable_symbols = [self.check_nullable(var) for var in production.split(" ")]
                return all(nullable_symbols)
            else:
                continue
        return False
    
    def is_unit_production(self, production: str) -> bool:
        return len(production.split(" ")) == 1 and self.is_variable_symbol(production)
    
    def can_derive_terminal(self, from_var: str, to_prod: str) -> bool:
        if len(to_prod.split(" ")) == 1 and self.is_terminal_symbol(to_prod):
            return True
        return False
    
    def convert_to_cnf(self, output_file=None):
        # Applying conversion rules to produce CNF from CFG
        self.remove_epsilon_productions()
        self.eliminate_unit_productions()
        self.reduce_long_productions()

        if output_file:
            with open(output_file, "w") as file:
                json.dump(self.grammar, file, indent=4)
        return self.grammar

    def remove_epsilon_productions(self):
        nullable_variables = [var for var in self.grammar["VARIABLES"] if self.check_nullable(var)]
        new_rules = {}

        for variable, productions in self.grammar["REGLAS"].items():
            new_productions = set(productions)
            for production in productions:
                symbols = production.split(" ")
                if any(sym in nullable_variables for sym in symbols):
                    self.add_nullable_combinations(new_productions, symbols, nullable_variables)
            new_rules[variable] = list(new_productions)
        self.grammar["REGLAS"] = new_rules

    def add_nullable_combinations(self, production_set, symbols, nullable_variables):
        for i in range(len(symbols)):
            if symbols[i] in nullable_variables:
                new_combination = symbols[:i] + symbols[i + 1:]
                if new_combination:
                    production_set.add(" ".join(new_combination))

    def eliminate_unit_productions(self):
        unit_pairs = [(var, prod) for var, prods in self.grammar["REGLAS"].items() for prod in prods if self.is_unit_production(prod)]
        while unit_pairs:
            from_var, unit = unit_pairs.pop()
            unit_productions = self.grammar["REGLAS"][unit]
            for prod in unit_productions:
                if prod not in self.grammar["REGLAS"][from_var]:
                    self.grammar["REGLAS"][from_var].append(prod)
                if self.is_unit_production(prod):
                    unit_pairs.append((from_var, prod))
            self.grammar["REGLAS"][from_var] = [p for p in self.grammar["REGLAS"][from_var] if not self.is_unit_production(p)]

    def reduce_long_productions(self):
        new_rules = {}
        new_variable_counter = 1
        for variable, productions in self.grammar["REGLAS"].items():
            new_productions = []
            for production in productions:
                symbols = production.split(" ")
                while len(symbols) > 2:
                    new_variable = f"X{new_variable_counter}"
                    new_variable_counter += 1
                    new_rules[new_variable] = [" ".join(symbols[:2])]
                    symbols = [new_variable] + symbols[2:]
                new_productions.append(" ".join(symbols))
            new_rules[variable] = new_productions
        self.grammar["REGLAS"].update(new_rules)
